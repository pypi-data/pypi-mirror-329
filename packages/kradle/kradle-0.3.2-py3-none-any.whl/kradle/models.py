# kradle/models.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TypedDict, NotRequired
from enum import Enum
from pprint import pformat
from dataclasses import asdict
import json



class MinecraftEvent(str, Enum):
    """
    Enumeration of all possible Minecraft bot event types captured from Mineflayer.
    
    This enum represents the various events that can occur during bot operation:
    - Idle state
    - Command execution
    - Chat and message interactions
    - Health-related events
    - Regular interval updates
    
    The event types correspond directly to Mineflayer bot events and are used to:
    1. Classify incoming events from the bot
    2. Trigger appropriate event handlers
    3. Update the observation state
    
    Event Sources:
        - bot.on('chat') -> CHAT
        - bot.on('message') -> MESSAGE
        - bot.on('health') -> HEALTH
        - bot.on('death') -> DEATH
        - Internal timer -> INTERVAL
        - Command system -> COMMAND_EXECUTED
        - Damage events -> DAMAGE
        - No active events -> IDLE
    
    Technical Details:
        - Inherits from str for JSON serialization
        - Used as a key field in Observation class
        - Maps directly to Mineflayer event system
        - Case-sensitive string values
    """
    IDLE = "idle"
    COMMAND_EXECUTED = "command_executed"
    CHAT = "chat"
    MESSAGE = "message"
    HEALTH = 'health'
    DEATH = "death"
    DAMAGE = "damage"
    INTERVAL = "interval"

class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"

class Weather(str, Enum):
    CLEAR = "clear"
    RAIN = "rain"
    THUNDER = "thunder"

class GameMode(str, Enum):
    SURVIVAL = "survival"
    CREATIVE = "creative"
    ADVENTURE = "adventure"
    SPECTATOR = "spectator"


# Agent method parameters

@dataclass
class ChatMessage:
    sender: str
    message: str

@dataclass
class ChallengeInfo:
    participant_id: str
    session_id: str
    task: str
    agent_modes: list
    commands: list
    js_functions: list
    available_events: list


@dataclass
class Observation:
    """
    Comprehensive representation of a Minecraft bot's state at a single point in time.
    Captures the complete state from the Mineflayer bot including location, surroundings,
    inventory, and events.

    Identity Attributes:
        name (str): Bot's username in the game
            Example: "Bot123"
        participant_id (str): Unique identifier for this bot instance
            Example: "uuid-1234-5678"
        session_id (str): Unique identifier for this session
            Example: "session-1234-5678"
        observation_id (str): Unique identifier for this specific observation
            Example: "obs-1234-5678"
        past_observation_id (Optional[str]): Reference to previous observation
            Example: "obs-1234-5677"

    Event Information:
        event (str): Current event type from EventType enum
            Example: "chat", "death", "idle"
        idle (bool): Whether bot is currently idle
            Example: True if no active tasks
        executing (Optional[str]): Command currently being executed
            Example: "move forward", None if no command
        output (Optional[str]): Output from last executed command
            Example: "Successfully moved to coordinates"

    Location Data:
        x (float): X coordinate in the world
            Example: 123.45
        y (float): Y coordinate (height) in the world
            Example: 64.0
        z (float): Z coordinate in the world
            Example: -789.01
        pitch (float): Vertical head rotation (-90 to 90)
            Example: 45.0
        yaw (float): Horizontal head rotation (-180 to 180)
            Example: 90.0

    Player State:
        health (float): Health points normalized to 0-1 range
            Example: 0.85 (17/20 hearts)
        hunger (float): Hunger points normalized to 0-1 range
            Example: 0.9 (18/20 food points)
        xp (float): Experience level
            Example: 30.0
        gamemode (GameMode): Current game mode enum
            Example: GameMode.SURVIVAL
        is_alive (bool): Whether bot is currently alive
            Example: True
        on_ground (bool): Whether bot is on solid ground
            Example: True
        equipped (str): Currently equipped item name
            Example: "diamond_sword"

    Environment State:
        biome (str): Current biome name
            Example: "plains", "desert", "forest"
        weather (Weather): Current weather enum
            Example: Weather.RAIN
        time (int): Minecraft time in ticks (0-24000)
            Example: 13000
        time_of_day (TimeOfDay): Time category enum
            Example: TimeOfDay.MORNING
        day_count (int): Number of in-game days passed
            Example: 42
        rain_state (float): Rain intensity from 0-1
            Example: 0.7
        thunder_state (float): Thunder intensity from 0-1
            Example: 0.0
        light_level (int): Block light level (0-15)
            Example: 14
        dimension (str): Current dimension name
            Example: "overworld", "nether", "end"

    World State:
        players (List[str]): Names of nearby players
            Example: ["Steve", "Alex"]
        blocks (List[str]): Visible block types in bot's range
            Example: ["stone", "dirt", "oak_log", "diamond_ore"]
        entities (List[str]): Nearby entity types
            Example: ["zombie", "sheep", "creeper"]
        craftable (List[str]): Items that can be crafted with current inventory
            Example: ["wooden_pickaxe", "torch", "crafting_table"]
        inventory (Dict[str, int]): Current inventory items and their counts
            Example: {"cobblestone": 64, "iron_ingot": 5}
        messages (List[ChatMessage]): Recent chat messages
            Example: [ChatMessage(role="player", content="Hello")]

    Data Sources:
        - Location: bot.entity.position
        - Health/Hunger: bot.health, bot.food
        - Inventory: bot.inventory.items()
        - Blocks: bot.findBlocks() with range of 64 blocks
        - Entities: bot.nearbyEntities with range of 64 blocks
        - Weather: bot.world.weatherData
        - Time: bot.time.timeOfDay
        - Messages: bot.chat events

    Methods:
        from_event(data: Dict) -> Observation:
            Creates new Observation from raw event data
        get_summary() -> str:
            Returns formatted summary of current state
        to_json() -> str:
            Returns JSON serialized state
        __str__() -> str:
            Returns formatted string representation
    """
    # Identity fields
    name: str = ""
    participant_id: str = ""
    session_id: str = ""
    observation_id: str = ""
    past_observation_id: Optional[str] = None

    # Event info
    event: str = "idle"
    idle: bool = True
    executing: Optional[str] = None
    output: Optional[str] = None

    # Location
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

    # Player state
    health: float = 1.0  # Normalized to 0-1 range
    hunger: float = 1.0  # Normalized to 0-1 range
    xp: float = 0.0
    gamemode: GameMode = GameMode.SURVIVAL
    is_alive: bool = True
    on_ground: bool = True
    equipped: str = ""

    # Environment
    biome: str = "plains"
    weather: Weather = Weather.CLEAR
    time: int = 0  # 0-24000
    time_of_day: TimeOfDay = TimeOfDay.MORNING
    day_count: int = 0
    rain_state: float = 0.0
    thunder_state: float = 0.0
    light_level: int = 15
    dimension: str = "overworld"

    # World state
    players: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    craftable: List[str] = field(default_factory=list)
    inventory: Dict[str, int] = field(default_factory=dict)
    messages: List[ChatMessage] = field(default_factory=list)

    @classmethod
    def from_event(cls, data: Dict) -> 'Observation':
        """Create state from event data with validation"""
        try:
            # Validate time range
            time = int(data.get('time', 0))
            if not 0 <= time <= 24000:
                time = time % 24000

            # Validate health/hunger are between 0-1
            health = float(data.get('health', 20))
            hunger = float(data.get('hunger', 20))
            health = max(0.0, min(1.0, health))
            hunger = max(0.0, min(1.0, hunger))

            return cls(
                # Identity
                name=str(data.get('name', '')),
                participant_id=str(data.get('participantId', '')),
                session_id=str(data.get('sessionId', '')),
                observation_id=str(data.get('observationId', '')),
                past_observation_id=data.get('past_observationid'),
                
                # Event
                event=str(data.get('event', 'idle')),
                idle=bool(data.get('idle', True)),
                executing=data.get('executing'),
                output=data.get('output'),
                
                # Location
                x=float(data.get('x', 0)),
                y=float(data.get('y', 0)),
                z=float(data.get('z', 0)),
                pitch=float(data.get('pitch', 0)),
                yaw=float(data.get('yaw', 0)),
                
                # Player State
                health=health,
                hunger=hunger,
                xp=float(data.get('xp', 0)),
                gamemode=GameMode(str(data.get('gamemode', 'survival'))),
                is_alive=bool(data.get('is_alive', True)),
                on_ground=bool(data.get('on_ground', True)),
                equipped=str(data.get('equipped', '')),
                
                # Environment
                biome=str(data.get('biome', 'plains')),
                weather=Weather(str(data.get('weather', 'clear'))),
                time=time,
                time_of_day=TimeOfDay(str(data.get('timeOfDay', 'morning'))),
                day_count=int(data.get('day_count', 0)),
                rain_state=float(data.get('rain_state', 0)),
                thunder_state=float(data.get('thunder_state', 0)),
                light_level=int(data.get('light_level', 15)),
                dimension=str(data.get('dimension', 'overworld')),
                
                # World State
                players=list(data.get('players', [])),
                blocks=list(data.get('blocks', [])),
                entities=list(data.get('entities', [])),
                craftable=list(data.get('craftable', [])),
                inventory=dict(data.get('inventory', {})),
                messages=[
                    ChatMessage(
                        sender=str(msg.get('sender', 'unknown')),
                        message=str(msg.get('message', ''))
                    ) 
                    for msg in data.get('messages', [])
                ]
            )
        except Exception as e:
            raise ValueError(f"Failed to parse state data: {str(e)}")

    def get_summary(self) -> str:
        """Returns a formatted summary of the observation state"""
        message_logs = '\n    - No messages' if not self.messages else ''.join(f'\n    - {msg.role}: {msg.content}' for msg in self.messages)
        
        return f"""Player Status:
            - Health: {self.health*100}%
            - Hunger: {self.hunger*100}%
            - XP Level: {self.xp}
            - Gamemode: {self.gamemode}
            - Is Alive: {self.is_alive}
            - Equipment: {self.equipped}

            Location & Environment:
            - Position: x={self.x}, y={self.y}, z={self.z}
            - Dimension: {self.dimension}
            - Biome: {self.biome}
            - Time: {self.time_of_day}
            - Weather: {self.weather}
            - Light Level: {self.light_level}

            World State:
            - Nearby Blocks: {', '.join(self.blocks) if self.blocks else 'None'}
            - Nearby Entities: {', '.join(self.entities) if self.entities else 'None'}
            - Craftable Items: {', '.join(self.craftable) if self.craftable else 'None'}
            - Inventory: {json.dumps(self.inventory) if self.inventory else 'Empty'}

            Chat Messages:{message_logs}

            Output from previous command: {self.output if self.output else 'None'}"""

    def __str__(self) -> str:
        """Clean, formatted string representation of all fields"""
        return pformat(asdict(self), indent=2, width=80, sort_dicts=False)

    def to_json(self) -> str:
        """Returns a JSON string representation of the observation."""
        return json.dumps(asdict(self), indent=4, default=str)


# Agent method responses

# We use TypedDicts instead of dataclasses for responses
# because they are much easier to serialize to JSON
class InitParticipantResponse(TypedDict):
    """The response from the server when an agent is initialized."""
    listenTo: List[str]
    # we may add more fields in the future

# TODO: type this
class OnEventResponse(Dict):
    pass

# class InitParticipantResponse(TypedDict):
#     """The response from the server when an agent is initialized."""
#     listenTo: List[str]
#     # we may add more fields in the future