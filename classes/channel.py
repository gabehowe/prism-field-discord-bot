from typing import Tuple, Union, Optional

import data_models.channel
from data_models.channel import ChannelType
from util import api_call


class Channel:
    __slots__: Tuple[str, ...] = (
        'id', 'type', 'guild_id', 'position', 'permission_overwrites', 'name', 'topic', 'nsfw',
        'last_message_id', 'bitrate', 'user_limit', 'rate_limit_per_user', 'recipients', 'icon', 'owner_id',
        'application_id', 'parent_id', 'last_pin_timestamp', 'rtc_region', 'video_quality_mode', 'message_count',
        'member_count', 'thread_metadata', 'member', 'default_auto_archive_duration', 'permissions')

    def __init__(self, data: data_models.channel.Channel):
        self.id: str = data.get('id')
        self.type: ChannelType = data_models.channel.ChannelType(data.get('type'))
        self.guild_id: Optional[str] = data.get('guild_id')
        self.position: Optional[int] = data.get('position')
        self.permission_overwrites: Optional[list] = data.get('permission_overwrites')
        self.name: Optional[str] = data.get('name')
        self.topic: Optional[str] = data.get('topic')
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
        """Computed permissions for the invoking user in the channel, including overwrites, only included when part of the resolved data received on a slash command interaction"""

    async def modify_channel(self, name=None, icon: bytes = None):
        json_object = {'name': name, 'icon': icon}
        await api_call(f'/channels/{self.id}', 'PATCH', json=json_object)
        if name is not None:
            self.name = name
        if icon is not None:
            self.icon = icon


class TextChannel(Channel):
    async def send(self, message):
        if message is None:
            return
        elif type(message) is dict:
            return await api_call(f'/channels/{self.id}/messages', 'POST', json=message)
        elif type(message) is str:
            return await api_call(f'/channels/{self.id}/messages', 'POST', json={"content": message})


async def get_channel(channel_id: str) -> Union[Channel, None, TextChannel]:
    channel_json = await api_call(f'/channels/{channel_id}')
    if channel_json is None:
        return None
    channel: Union[Channel, TextChannel] = Channel(channel_json)
    if channel.type in [ChannelType.GUILD_TEXT, ChannelType.DM, ChannelType.GROUP_DM, ChannelType.GUILD_NEWS,
                        ChannelType.GUILD_STORE, ChannelType.GUILD_PUBLIC_THREAD, ChannelType.GUILD_PRIVATE_THREAD]:
        channel = TextChannel(channel_json)
    return channel
