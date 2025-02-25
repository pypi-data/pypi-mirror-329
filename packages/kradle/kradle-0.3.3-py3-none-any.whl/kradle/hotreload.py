from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib.util
import sys
import os
import time
import traceback
from typing import Dict, Optional, ClassVar
import threading

class AgentReloader(FileSystemEventHandler):
    _observers: ClassVar[Dict[str, Observer]] = {}
    _lock = threading.Lock()

    def __init__(self, kradle_instance, agent_module_path, agent_class):
        self.kradle_instance = kradle_instance
        self.agent_module_path = agent_module_path
        self.agent_class_name = agent_class.__name__
        self.last_reload = 0
        self.reload_cooldown = 1

    def on_modified(self, event):
        if event.src_path == self.agent_module_path:
            current_time = time.time()
            if current_time - self.last_reload > self.reload_cooldown:
                self.last_reload = current_time
                self.reload_agent()

    def reload_agent(self):
        try:
            module_name = os.path.splitext(os.path.basename(self.agent_module_path))[0]
            
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            spec = importlib.util.spec_from_file_location(module_name, self.agent_module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, self.agent_class_name):
                new_agent_class = getattr(module, self.agent_class_name)
                
                for username, info in self.kradle_instance._agent_classes.items():
                    if info['class'].__name__ == self.agent_class_name:
                        # Update the class reference
                        info['class'] = new_agent_class
                        
                        # Update all existing instances of this agent
                        for participant_id, agent in list(self.kradle_instance._agents.items()):
                            if isinstance(agent, info['class'].__bases__[0]):  # Check if it's an instance of the base class
                                # Create new instance
                                new_agent = new_agent_class(username=agent.username)
                                new_agent.participant_id = agent.participant_id
                                
                                # Copy over any important instance attributes
                                if hasattr(agent, 'memory'):
                                    new_agent.memory = agent.memory
                                
                                # Replace the old instance
                                self.kradle_instance._agents[participant_id] = new_agent
                        
                        self.kradle_instance._logger.log_success(
                            f"🔄 Hot reloaded: {self.agent_class_name}"
                        )
                        return
            
        except Exception as e:
            self.kradle_instance._logger.log_error(
                f"Hot reload failed: {str(e)}"
            )

def setup_hot_reload(kradle_instance, agent_class) -> Optional[Observer]:
    """Sets up hot reloading for the agent class."""
    try:
        agent_module = sys.modules[agent_class.__module__]
        if not hasattr(agent_module, '__file__'):
            return None

        agent_module_path = os.path.abspath(agent_module.__file__)
        watch_dir = os.path.dirname(agent_module_path)

        with AgentReloader._lock:
            if watch_dir in AgentReloader._observers:
                return AgentReloader._observers[watch_dir]

            event_handler = AgentReloader(kradle_instance, agent_module_path, agent_class)
            observer = Observer()
            observer.schedule(event_handler, watch_dir, recursive=False)
            observer.start()
            AgentReloader._observers[watch_dir] = observer
            
            return observer
        
    except Exception as e:
        kradle_instance._logger.log_error(f"Hot reload setup failed: {str(e)}")
        return None