from typing import TypedDict


class RoleTags(TypedDict, total=False):
    bot_id: str
    integration_id: str
    premium_subscriber: None


class _RoleOptional(TypedDict, total=False):
    tags: RoleTags


class Role(_RoleOptional):
    id: str
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
