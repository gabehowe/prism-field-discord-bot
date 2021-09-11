from typing import Tuple, Optional

from classes.channel import TextChannel
from classes.guild import Guild
from classes.member import GuildMember, User
from classes.permissions import Permissions
from classes.slashcommandmanager import ApplicationCommandData
from data_models import interaction
from data_models.interaction import InteractionResponse
from util import api_call


class Interaction:
    __slots__: Tuple[str, ...] = (
        'id', 'application_id', 'type', 'data', 'guild_id', 'channel', 'member', 'user', 'token', 'version',
        'message', 'bot', 'guild')

    def __init__(self, data: interaction.Interaction):
        self.id = data.get('id')
        self.application_id = data.get('application_id')
        self.type = data.get('type')
        self.guild_id = data.get('guild_id')
        self.guild: Optional[Guild] = None
        self.token = data.get('token')
        self.version = data.get('version')
        self.message = data.get('message')
        self.channel: Optional[TextChannel] = None
        self.bot: Optional[GuildMember] = None
        if 'data' in data:
            self.data = ApplicationCommandData(data.get('data'))
        if 'member' in data:
            self.member = GuildMember(data.get('member'))
        if 'user' in data:
            self.user = User(data.get('user'))

    async def async_init(self, data: interaction.Interaction, client):
        if 'guild_id' in data:
            request = await api_call(f'/guilds/{self.guild_id}/members/{client.bot.id}')

            guilds = await api_call('/users/@me/guilds')
            request_guild = Guild(request)
            if guilds is None:
                return
            for i in guilds:
                guild = Guild(i)
                client.guilds[guild.id].permissions = guild.permissions
            request_guild.permissions = client.guilds[data['guild_id']].permissions
            request['permissions'] = request_guild.permissions
            self.guild = client.guilds[data['guild_id']]
            self.bot = GuildMember(request)
        if 'channel_id' in data:
            self.channel = TextChannel(await api_call(f'/channels/{data.get("channel_id")}'))
        return self

    async def reply(self, response, ephemeral: bool = False):
        if response is None:
            return
        elif isinstance(response, dict):
            return await api_call(f'/interactions/{self.id}/{self.token}/callback', "POST", json=response)
        elif type(response) is str:
            flags = 64 if ephemeral else None
            reply: InteractionResponse = {'type': 4, 'data': {'content': response, 'flags': flags}}
            await self.reply(reply)

    async def error(self, extra: str = None):
        if extra is not None:
            await self.reply('There was an error executing this command: ' + extra, True)
        else:
            await self.reply('There was an error executing this command.', True)

    async def no_permission_user(self, extra: Permissions = None):
        if extra is not None:
            await self.reply(f'You need the `{extra.name}` permission to use this.', True)
        else:
            await self.reply('You don\'t have permission to use this.', True)

    async def no_permission_bot(self, extra: Permissions = None):
        if extra is not None:
            await self.reply(f'I need the `{extra.name}` permission to use this.', True)
        else:
            await self.reply('I don\'t have permission to use this.', True)

    async def in_dev(self):
        await self.reply('This feature is in development.', True)

    async def ack_component(self):
        await api_call(f'/interactions/{self.id}/{self.token}/callback', 'POST', json={'type': 6})
