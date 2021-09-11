from typing import Tuple

import data_models.channel
from util import api_call


class Channel:
    __slots__: Tuple[str, ...] = (
        'id', 'type', 'guild_id', 'position', 'permission_overwrites', 'name', 'topic', 'nsfw',
        'last_message_id', 'bitrate', 'user_limit', 'rate_limit_per_user', 'recipients', 'icon', 'owner_id',
        'application_id', 'parent_id', 'last_pin_timestamp', 'rtc_region', 'video_quality_mode', 'message_count',
        'member_count', 'thread_metadata', 'member', 'default_auto_archive_duration', 'permissions')

    def __init__(self, data: data_models.channel.Channel):
        self.id = data.get('id')
        self.type = data_models.channel.ChannelType(data.get('type'))
        self.guild_id = data.get('guild_id')
        self.position = data.get('position')
        self.permission_overwrites = data.get('permission_overwrites')
        self.name = data.get('name')
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw')
        self.last_message_id = data.get('last_message_id')
        self.bitrate = data.get('bitrate')
        self.user_limit = data.get('user_limit')
        self.rate_limit_per_user = data.get('rate_limit_per_user')
        self.recipients = data.get('recipients')
        self.icon = data.get('icon')
        self.owner_id = data.get('owner_id')
        self.application_id = data.get('application_id')
        self.parent_id = data.get('parent_id')
        self.last_pin_timestamp = data.get('last_pin_timestamp')
        self.rtc_region = data.get('rtc_region')
        self.video_quality_mode = data.get('video_quality_mode')
        self.message_count = data.get('message_count')
        self.member_count = data.get('member_count')
        self.thread_metadata = data.get('thread_metadata')
        self.member = data.get('member')
        self.default_auto_archive_duration = data.get('default_auto_archive_duration')
        self.permissions = data.get('permissions')


class TextChannel(Channel):
    async def send(self, message):
        if message is None:
            return
        elif type(message) is dict:
            return await api_call(f'/channels/{self.id}/messages', 'POST', json=message)
        elif type(message) is str:
            return await api_call(f'/channels/{self.id}/messages', 'POST', json={"content": message})
