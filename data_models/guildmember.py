from typing import TypedDict, Optional

import data_models.user


class _GuildMemberOptional(TypedDict, total=False):
    user: data_models.user.User
    nick: Optional[str]
    premium_since: Optional[str]
    pending: bool
    permissions: str


class GuildMember(_GuildMemberOptional):
    roles: list
    joined_at: str
    deaf: bool
    mute: bool
