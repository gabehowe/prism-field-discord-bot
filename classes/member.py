from typing import List
from typing import Tuple

import data_models.user
import util
from classes import permissions
from classes.channel import TextChannel
from classes.role import Role
from data_models import guildmember
from util import api_call


class GuildMember:
    def __init__(self, data: guildmember.GuildMember):
        if 'user' in data:
            self.user = User(data.get('user'))
        self.nick = data.get('nick')
        if 'roles' in data:
            self.roles: List[Role] = []
            for i in data.get('roles'):
                self.roles.append(Role(i))
        self.joined_at = util.parse_time(data.get('joined_at'))
        self.premium_since = util.parse_time(data.get('premium_since'))
        self.deaf = data.get('deaf')
        self.mute = data.get('mute')
        self.pending = data.get('pending')
        self.permissions_int = data.get('permissions')
        if self.permissions_int is not None:
            self.permissions_int = int(self.permissions_int)
            self.permissions_list: List[permissions.Permissions] = []
            for i in permissions.Permissions:
                if self.permissions_int & int(i.value) == int(i.value):
                    self.permissions_list.append(i)

    async def add_role(self, role_id: str, guild_id: str):
        await api_call(f'/guilds/{guild_id}/members/{self.user.id}/roles/{role_id}', 'PUT')

    async def remove_role(self, role_id: str, guild_id: str):
        await api_call(f'/guilds/{guild_id}/members/{self.user.id}/roles/{role_id}', 'DELETE')


async def get_user(user_id: str):
    user_json = await api_call(f'/users/{user_id}')
    return User(user_json)


class User:
    __slots__: Tuple[str, ...] = (
        'id', 'username', 'discriminator', 'avatar', 'bot', 'system', 'mfa_enabled', 'locale', 'verified', 'email',
        'flags', 'premium_type', 'public_flags')

    def __init__(self, data: data_models.user.User):
        self.id = data.get('id')
        self.username = data.get('username')
        self.discriminator = data.get('discriminator')
        self.avatar = data.get('avatar')
        self.bot = data.get('bot')
        self.system = data.get('system')
        self.mfa_enabled = data.get('mfa_enabled')
        self.locale = data.get('locale')
        self.verified = data.get('verified')
        self.email = data.get('email')
        self.flags = data.get('flags')
        self.premium_type = data.get('premium_type')
        self.public_flags = data.get('public_flags')

    async def get_dm_channel(self):
        return TextChannel(await api_call('/users/@me/channels', 'POST', json={"recipient_id": self.id}))

    async def dm(self, message):
        if message is None:
            return
        elif type(message) is dict or type(message) is str:
            channel = await self.get_dm_channel()
            return await channel.send(message)
