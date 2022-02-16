import enum
from typing import TypedDict, List, Dict

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


class InteractionType(enum.IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


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
    values: list
    target_id: str


class ApplicationCommandInteractionData(_ApplicationCommandInteractionDataOptional):
    id: str
    name: str
    type: int
    custom_id: str
    component_type: int
    components: List[dict]


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


class ComponentType(enum.IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4


class ActionRow(TypedDict):
    type: int  # should be 1
    components: List[dict]


class ButtonStyle(enum.IntEnum):
    BLURPLE = 1
    GREY = 2
    GREEN = 3
    DANGER = 4
    LINK = 5


class _ButtonOptional(TypedDict, total=False):
    label: str
    emoji: dict
    custom_id: str
    url: str
    disabled: bool


class Button(_ButtonOptional):
    type: int  # should be 2
    style: ButtonStyle


class _SelectOptionOptional(TypedDict, total=False):
    description: str
    emoji: dict
    default: bool


class SelectOption(_SelectOptionOptional):
    label: str
    value: str


class _SelectMenuOptional(TypedDict, total=False):
    placeholder: str
    min_values: int
    max_values: int
    disabled: bool


class SelectMenu(_SelectMenuOptional):
    type: int  # should be 3
    custom_id: str
    options: List[SelectOption]


class TextInputStyle(enum.IntEnum):
    SHORT = 1
    PARAGRAPH = 2


class _TextInputOptional(TypedDict, total=False):
    min_length: int
    max_length: int
    required: bool
    value: str
    placeholder: str


class TextInput(_TextInputOptional):
    type: int  # should be 4
    custom_id: str
    style: TextInputStyle
    label: str
