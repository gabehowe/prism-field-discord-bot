import enum
from typing import TypedDict, Optional, List

from data_models.user import User


class _ChannelOptional(TypedDict, total=False):
    guild_id: str
    position: int
    permission_overwrites: list
    name: str
    topic: Optional[str]
    nsfw: bool
    last_message_id: Optional[str]
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: List[User]
    icon: Optional[str]
    owner_id: str
    application_id: str
    parent_id: Optional[str]
    last_pin_timestamp: Optional[str]
    rtc_region: Optional[str]
    video_quality_mode: Optional[str]
    message_count: int
    member_count: int
    thread_metadata: object
    member: object
    default_auto_archive_duration: int
    permissions: str


class ChannelTypeType(enum.Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13


class ChannelType(_ChannelOptional):
    id: str
    type: ChannelTypeType
