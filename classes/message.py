import datetime

import dateutil.parser

from classes.member import User, load_user, load_guild_member


class Message:

    def __init__(self):
        self.id = None
        self.channel_id = None
        self.guild_id = None
        self.author = None
        self.member = None
        self.content = None
        self.timestamp = None  # type: datetime
        self.edited_timestamp = None
        self.tts = None
        self.mention_everyone = None
        self.mentions = None
        self.mention_roles = None
        self.mention_channels = None
        self.attachments = None
        self.embeds = None
        self.reactions = None
        self.nonce = None
        self.pinned = None
        self.webhook_id = None
        self.type = None
        self.activity = None
        self.application = None
        self.application_id = None
        self.message_reference = None
        self.flags = None
        self.referenced_message = None
        self.interaction = None
        self.thread = None
        self.components = None
        self.sticker_items = None
        self.stickers = None


async def load_message(data: dict):
    message = Message()
    message.id = data.get('id')
    message.channel_id = data.get('channel_id')
    message.guild_id = data.get('guild_id') if 'guild_id' in data.keys() else None
    message.author = await load_user(data.get('author'))
    message.member = await load_guild_member(data.get('member')) if 'member' in data.keys() else None
    message.content = data.get('content')
    message.timestamp = dateutil.parser.parse(str(data.get('timestamp')))
    if data.get('premium_since') is None:
        message.edited_timestamp = None
    else:
        message.edited_timestamp = dateutil.parser.parse(
            data.get('edited_timestamp'))
    message.tts = bool(data.get('tts'))
    message.mention_everyone = bool(data.get('mention_everyone'))
    message.mentions = data.get('mentions')
    message.mention_roles = data.get('mention_roles')
    message.mention_channels = data.get('mention_channels') or None
    message.attachments = data.get('attachment')
    message.embeds = data.get('embeds')
    message.reactions = data.get('reactions') or None
    message.nonce = data.get('nonce') or None
    message.pinned = data.get('pinned')
    message.webhook_id = data.get('webhook_id')
    message.type = data.get('type') or None
    message.activity = data.get('activity') or None
    message.application = data.get('application') or None
    message.application_id = data.get('application_id') or None
    message.message_reference = data.get('message_reference') or None
    message.flags = data.get('flags') or None
    message.referenced_message = data.get('referenced_message') or None
    message.interaction = data.get('interaction') or None
    message.thread = data.get('thread') or None
    message.components = data.get('components') or None
    message.sticker_items = data.get('sticker_items') or None
    message.stickers = data.get("stickers") or None
    return message
