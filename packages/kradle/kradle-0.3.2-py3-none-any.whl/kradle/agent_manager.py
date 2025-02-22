import sys
from flask import Flask, jsonify, request
import threading
import socket
from werkzeug.serving import make_server
import signal
from flask_cors import CORS
from kradle.models import ChallengeInfo, Observation
from kradle.logger import KradleLogger
from kradle.ssh_tunnel import create_tunnel
from kradle.api.client import KradleAPI
from kradle.api.http import KradleAPIError
from kradle.hotreload import setup_hot_reload
from kradle.core import MinecraftAgent
import kradle.utils as utils

class AgentManager:
    """
    The agent manager creates a server to expose the agent. It handles the lifecycle
    of creating and managing instances of the provided agent class for each participant
    in a challenge.

    The AgentManager class is a singleton (i.e. the class itself behaves as a single instance).
    """
    _instance = None
    _server = None
    _server_ready = threading.Event()
    _shutdown_event = threading.Event()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance._agents = {}  # participant_id -> agent instance
            cls._instance._agent_classes = {}  # username -> {class: agent_class, count: int}
            cls._instance._app = None
            cls._instance.port = None
            cls._instance._api_client = KradleAPI()
            cls._instance._server_thread = None
            cls._instance._main_thread = None
            cls._instance._logger = KradleLogger()
        return cls._instance

    def _is_port_available(self, port, host='localhost'):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                return True
        except OSError:
            return False

    def _find_free_port(self, start_port=1500, end_port=1549):
        for port in range(start_port, end_port + 1):
            if self._is_port_available(port):
                return port
        raise RuntimeError(f"No free ports available in range {start_port}-{end_port}")

    def _get_or_create_agent(self, participant_id, username) -> MinecraftAgent:
        if participant_id in self._agents:
            return self._agents[participant_id]

        if username is None:
            if not self._agent_classes:
                raise ValueError("No agent classes registered")
            username = next(iter(self._agent_classes))

        if username in self._agent_classes:
            agent_class = self._agent_classes[username]['class']
        else:        
            if "*" in self._agent_classes:
                agent_class = self._agent_classes["*"]['class']
            else:
                raise ValueError(f"No agent class registered for username: {username}, no catch-all agent found")
        
        agent = agent_class(api_client=self._api_client)
        self._agents[participant_id] = agent
            
        return self._agents[participant_id]

    def _get_instance_counts(self, username=None):
        if username:
            if username not in self._agent_classes:
                return None
            class_name = self._agent_classes[username]['class'].__name__
            count = self._agent_classes[username]['count']
            return {'class_name': class_name, 'instances': count}
            
        counts = {}
        for username, info in self._agent_classes.items():
            counts[username] = {
                'class_name': info['class'].__name__,
                'instances': info['count']
            }
        return counts

    def _create_app(self):
        app = Flask(__name__)
        app.config['DEBUG'] = True
        app.config['ENV'] = 'development'
        CORS(app)

        @app.after_request
        def after_request(response):
            self._logger.log_api_call(
                request.method,
                request.path,
                response.status_code
            )
            return response

        @app.route('/')
        def index():
            base_url = f"http://localhost:{self.port}"
            response = {
                'status': 'online',
                'agents': {},
            }
            
            for username in self._agent_classes.keys():
                agent_urls = {
                    'base': f"{base_url}/{username}",
                    'ping': f"{base_url}/{username}/ping",
                    'init': f"{base_url}/{username}/init",
                    'event': f"{base_url}/{username}/event"
                }
                response['agents'][username] = agent_urls
                
            return jsonify(response)

        @app.route('/<username>')
        def agent_index(username):
            if username not in self._agent_classes:
                return '', 404
                
            base_url = f"http://localhost:{self.port}/{username}"
            stats = self._get_instance_counts(username)
            
            return jsonify({
                'status': 'online',
                'class_name': stats['class_name'],
                'instances': stats['instances'],
                'urls': {
                    'ping': f"{base_url}/ping",
                    'init': f"{base_url}/init",
                    'event': f"{base_url}/event"
                }
            })

        @app.route('/ping', defaults={'username': None})
        @app.route('/<username>/ping')
        def ping(username):
            if username:
                if username not in self._agent_classes:
                    return '', 404
                stats = self._get_instance_counts(username)
                return jsonify({
                    'status': 'online',
                    'class_name': stats['class_name'],
                    'instances': stats['instances']
                })

            return jsonify({
                'status': 'online',
                'agents': self._get_instance_counts()
            })

        @app.route('/init', defaults={'username': None}, methods=['POST'])
        @app.route('/<username>/init', methods=['POST'])
        def init(username):
            data = request.get_json() or {}
            participant_id = data.get('participantId')

            if participant_id is None:
                self._logger.log_error("Missing participantId in init request")
                return jsonify({'error': 'participantId is required'}), 400

            try:
                agent = self._get_or_create_agent(participant_id, username)
                # Inject participant and session IDs to the agent
                agent.participant_id = participant_id
                agent.session_id = data.get('sessionId')

                # TODO: initialize memory here

                # run agent.init_participant()
                challenge_info = ChallengeInfo(
                    participant_id=participant_id,
                    session_id=data.get('sessionId'),
                    task=data.get('task'),
                    agent_modes=data.get('agent_modes'),
                    commands=data.get('commands'),
                    js_functions=data.get('js_functions'),
                    available_events=data.get('available_events')
                )
                init_data = agent.init_participant(challenge_info)
                self._logger.log_success(f"Agent initialized for participant {participant_id}")

                # TODO: if the API accepts 'listenTo', then we can
                # just return jsonify(init_data) below
                return jsonify({'choices': init_data['listenTo']})
            except ValueError as e:
                self._logger.log_error(f"Failed to initialize agent: {str(e)}")
                return jsonify({'error': str(e)}), 400

        @app.route('/event', defaults={'username': None}, methods=['POST'])
        @app.route('/<username>/event', methods=['POST'])
        def event(username):
            data = request.get_json() or {}
            observation = Observation.from_event(data)
            participant_id = data.get('participantId')
            
            if participant_id is None:
                self._logger.log_error("Missing participantId in event request")
                return jsonify({'error': 'participantId is required'}), 400

            try:
                agent = self._get_or_create_agent(participant_id, username)
                result = agent.on_event(observation)
                return jsonify(result)
            except ValueError as e:
                self._logger.log_error("Error in event handler", e)
                return jsonify({'error': str(e)}), 400
            
        return app

    def _run_server(self):
        try:
            self._server = make_server('0.0.0.0', self.port, self._app)
            self._server_ready.set()
            self._server.serve_forever()
        except Exception as e:
            self._logger.log_error("Server crashed", e)
            self._shutdown_event.set()
            raise e
            
    def _setup_signal_handlers(self):
        def handle_shutdown(signum, frame):
            self._logger.on_shutdown()
            self._shutdown_event.set()
            if self._server:
                self._server.shutdown()
        
        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)
    
    def _get_tunnel_url(self, port):
        if hasattr(self, '_tunnel_url') and self._tunnel_url:
            return self._tunnel_url
        
        tunnel_instance, tunnel_url = create_tunnel(port)
        if tunnel_instance:
            self._logger.log_success(f"Public URL (tunnel) created successfully")
            self._tunnel_url = tunnel_url
            return tunnel_url
        else:
            raise Exception("Failed to create a public URL (tunnel)")
    
    def _validate_api_key(self):
        """Validate the API key and print a helpful error message if it's not set."""
        try:
            self._api_client.validate_api_key()
        except Exception as e:
            # If it's still not set, then log an error and raise an exception
            self._logger.log_error(
                f"\n> API key required\n\n"
                f"Setup:\n"
                f"  1. Get your key: https://app.kradle.ai\n"
                f"  2. EITHER set the KRADLE_API_KEY environment variable as your key\n"
                f"     OR use `{self.__class__.__name__}.set_api_key(API_KEY)` to set it\n"
            )
            raise e
    @classmethod
    def set_api_key(cls, api_key):
        """
        Set the API key for the agent manager.

        This method does not need to be called if the KRADLE_API_KEY environment variable is set.
        """
        instance = cls()
        instance._api_client.set_api_key(api_key)

    @classmethod
    def serve(cls, agent_class, create_public_url=False, public_url=None, host='localhost', port=None, hot_reload=True):
        """Start the agent server with automatic agent instance lifecycle support."""
        instance = cls()

        # Initial setup
        instance._validate_api_key()
        port = port if port is not None else instance._find_free_port()
        
        # Get the agent username
        username = agent_class.username

        print(f"username: {username}")

        # Get the agent URL
        if public_url:
            agent_url = public_url
        elif create_public_url:
            agent_url = f"{instance._get_tunnel_url(port)}/{username}"
        else:
            agent_url = f"http://{host}:{port}/{username}" 
        
        # If a public URL was provided or created, then update the agent's
        # URL on Kradle.
        if public_url or create_public_url:
            try:
                # Let's first assume the agent already exists
                try:
                    instance._api_client.agents.update(
                        username,
                        url=agent_url,
                    )
                    instance._logger.log_success(f"Agent '{username}' updated successfully")
                except KradleAPIError as e:
                    if e.status_code == 404:
                        # The agent doesn't already exist, so we'll create it
                        instance._logger.log_info(f"Agent '{username}' not found, creating it")
                        instance._api_client.agents.create(
                            username,
                            name= agent_class.display_name or agent_class.__name__,
                            url=agent_url,
                            description= agent_class.description or "Created by the Kradle Python SDK",
                        )
                        instance._logger.log_success(f"Agent '{username}' created successfully")
                    else:
                        raise e
            except Exception as e:
                instance._logger.log_error(f"Failed to create/update agent '{username}'", e)
                sys.exit(1)

        # Handle hot reload case
        is_hot_reload = username in instance._agent_classes and hasattr(agent_class, 'url')
        if is_hot_reload:
            instance._agent_classes[username]['class'] = agent_class
            if hot_reload:
                instance._hot_reload_observer = setup_hot_reload(instance, agent_class)
            return agent_class.url

        # Register new agent class
        if username not in instance._agent_classes:
            instance._agent_classes[username] = {'class': agent_class, 'count': 1}

        # Initialize or use existing server
        if not instance._app:
            # Set up new server
            instance._app = instance._create_app()
            instance.port = port
            utils.setup_server(instance, port, host)
            
            # Set agent properties
            if username != "*":
                agent_class.url = agent_url
                agent_class.username = username

            if hot_reload:
                instance._hot_reload_observer = setup_hot_reload(instance, agent_class)

            # Display startup banner
            instance._logger.display_startup_banner({
                'env': instance._app.config['ENV'],
                'debug': instance._app.config['DEBUG'],
                'port': instance.port,
                'agent_username': username,
                'agent_url': agent_url,
                'challenge_url': f'{instance._api_client.base_url}workbench/challenges'
            })
            
            # Start main thread
            instance._main_thread = threading.Thread(target=instance._shutdown_event.wait)
            instance._main_thread.daemon = False
            instance._main_thread.start()
            
            return agent_url
        
        # Handle existing server case
        if username != "*":
            agent_class.url = agent_url
            agent_class.username = username

        if hot_reload:
            instance._hot_reload_observer = setup_hot_reload(instance, agent_class)
            
        return agent_url
