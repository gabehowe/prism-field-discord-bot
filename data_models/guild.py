from typing import TypedDict, Optional, List

from data_models.channel import Channel
from data_models.guildmember import GuildMember
from data_models.roles import Role


class _GuildOptional(TypedDict, total=False):
    icon_hash: Optional[str]
    owner: bool
    permissions: str
    region: Optional[str]
    widget_enabled: bool
    widget_channel_id: Optional[str]
    joined_at: str
    large: bool
    unavailable: bool
    member_count: int
    voice_states: list
    members: List[GuildMember]
    channels: List[Channel]
    threads: List[Channel]
    presences: list
    max_presences: Optional[int]
    max_members: int
    premium_subscription_count: int
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: dict
    stage_instances: List[dict]
    stickers: List[dict]


class Guild(_GuildOptional):
    id: str
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    owner_id: str
    afk_channel_id: Optional[str]
    afk_timeout: int
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: List[Role]
    emojis: List[dict]  # TODO add emoji object
    features: List[str]
    mfa_level: int
    application_id: Optional[str]
    system_channel_id: Optional[str]
    system_channel_flags: int
    rules_channel_id: Optional[str]
    vanity_url_code: Optional[str]
    description: Optional[str]
    banner: Optional[str]
    premium_tier: int
    preferred_locale: str
    public_updates_channel_id: Optional[str]
    nsfw_level: int
