import enum
from typing import TypedDict, Optional, List


class Status(str, enum.Enum):
    ONLINE = 'online'
    DND = 'dnd'
    IDLE = 'idle'
    INVISIBLE = 'invisible'
    OFFLINE = 'offline'


class ActivityType(enum.IntEnum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5


class _ActivityOptional(TypedDict, total=False):
    url: Optional[str]


class Activity(_ActivityOptional):
    name: str
    type: ActivityType


class GatewayPresenceUpdate(TypedDict):
    since: Optional[int]
    activities: List[Activity]
    status: Status
    afk: bool
