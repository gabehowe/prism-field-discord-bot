from typing import TypedDict, Optional


class _UserOptional(TypedDict, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    locale: str
    verified: bool
    email: Optional[str]
    flags: int
    premium_type: int
    public_flags: int


class User(_UserOptional):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]
