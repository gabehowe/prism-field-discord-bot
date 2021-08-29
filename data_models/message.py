from typing import TypedDict, Optional, Any, Union

import data_models.user
from data_models.guildmember import GuildMember


class _MessageOptional(TypedDict, total=False):
    guild_id: str
    member: GuildMember
    mention_channels: list
    reactions: list
    nonce: Union[int, str]
    webhook_id: str
    activity: dict  # TODO make a message activity type
    application: dict  # TODO make an application object
    application_id: str
    message_reference: dict  # TODO make a message reference object
    flags: int
    referenced_message: dict
    interaction: dict  # TODO make a interaction data type
    thread: dict  # TODO make a channel object
    components: list
    sticker_items: list
    stickers: list


class Message(_MessageOptional):
    id: str
    channel_id: str
    author: data_models.user.User
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: list
    mention_roles: list
    attachments: list
    embeds: list
    pinned: bool
    type: int


class SendingMessage(TypedDict, total=False):
    content: str
    tts: bool
    file: dict
    embeds: list  # TODO add embed object
    embed: dict
    payload_json: str
    allowed_mentions: dict  # TODO add allowed mentions object
    message_reference: dict  # TODO add message reference object
    components: list  # TODO add message component object
    sticker_ids: list
