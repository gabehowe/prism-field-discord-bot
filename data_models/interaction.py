import enum
from typing import Optional, TypedDict, List, Dict

from data_models.guildmember import GuildMember
from data_models.message import Message
from data_models.user import User


class _InteractionResponseOptionalData(TypedDict, total=False):
    tts: bool
    content: str
    embeds: List[dict]  # TODO add embed object
    components: list
    flags: int
    ephemeral: bool
    allowed_mentions: dict


class _InteractionResponseOptional(TypedDict, total=False):
    data: _InteractionResponseOptionalData


class InteractionResponse(_InteractionResponseOptional):
    type: int


class ApplicationCommandOptionType(enum.Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10


class InteractionType(enum.Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


class _ApplicationCommandInteractionDataOptionOptional(TypedDict, total=False):
    value: ApplicationCommandOptionType
    options: List[dict]


class ApplicationCommandInteractionDataOption(_ApplicationCommandInteractionDataOptionOptional):
    name: str
    type: ApplicationCommandOptionType


class ApplicationCommandInteractionDataResolved(TypedDict, total=False):
    users: Dict[str, User]
    members: Dict[str, GuildMember]
    roles: Dict[str, dict]  # TODO add roles data model
    channels: Dict[str, dict]  # TODO add channels data model


class _ApplicationCommandInteractionDataOptional(TypedDict, total=False):
    resolved: ApplicationCommandInteractionDataResolved
    options: List[ApplicationCommandInteractionDataOption]


class ApplicationCommandInteractionData(_ApplicationCommandInteractionDataOptional):
    id: str
    name: str
    custom_id: str
    component_type: int


class _InteractionOptional(TypedDict, total=False):
    data: ApplicationCommandInteractionData
    guild_id: str
    channel_id: str
    member: GuildMember
    user: User
    message: Message


class Interaction(_InteractionOptional):
    id: str
    application_id: str
    type: InteractionType
    token: str
    version: int
