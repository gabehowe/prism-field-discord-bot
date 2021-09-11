from typing import Optional

import data_models.message
import util
from classes.channel import TextChannel
from classes.member import User, GuildMember


class Message(object):

    def __init__(self, data: data_models.message.Message):
        self.id = data.get('id')
        self.guild_id = data.get('guild_id') if 'guild_id' in data.keys() else None
        self.author: Optional[User] = User(data.get('author'))
        self.member = GuildMember(data.get('member')) if 'member' in data.keys() else None
        self.content = data.get('content')
        self.timestamp = util.parse_time(data.get('timestamp'))
        self.edited_timestamp = util.parse_time(data.get('edited_timestamp'))
        self.tts = bool(data.get('tts'))
        self.mention_everyone = bool(data.get('mention_everyone'))
        self.mentions = data.get('mentions')
        self.mention_roles = data.get('mention_roles')
        self.mention_channels = data.get('mention_channels')
        self.attachments = data.get('attachments')
        self.embeds = data.get('embeds')
        self.reactions = data.get('reactions')
        self.nonce = data.get('nonce')
        self.pinned = data.get('pinned')
        self.webhook_id = data.get('webhook_id')
        self.type = data.get('type')
        self.activity = data.get('activity')
        self.application = data.get('application')
        self.application_id = data.get('application_id')
        self.message_reference = data.get('message_reference')
        self.flags = data.get('flags')
        self.referenced_message = data.get('referenced_message')
        self.interaction = data.get('interaction')
        self.thread = data.get('thread')
        self.components = data.get('components')
        self.sticker_items = data.get('sticker_items')
        self.stickers = data.get("stickers")
        self.channel = None

    async def async_init(self, data: data_models.message.Message):
        if 'channel_id' in data:
            self.channel = TextChannel(await util.api_call(f'/channels/{data.get("channel_id")}'))
        return self
