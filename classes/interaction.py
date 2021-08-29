from typing import Tuple

from classes.member import GuildMember, User
from classes.permissions import Permissions
from classes.slashcommandmanager import ApplicationCommandData
from data_models import interaction
from data_models.interaction import InteractionResponse
from util import api_call


class Interaction:
    __slots__: Tuple[str, ...] = (
        'id', 'application_id', 'type', 'data', 'guild_id', 'channel_id', 'member', 'user', 'token', 'version',
        'message')

    def __init__(self, data: interaction.Interaction):
        self.id = data.get('id')
        self.application_id = data.get('application_id')
        self.type = data.get('type')
        self.guild_id = data.get('guild_id')
        self.channel_id = data.get('channel_id')
        self.token = data.get('token')
        self.version = data.get('version')
        self.message = data.get('message')
        if 'data' in data:
            self.data = ApplicationCommandData(data.get('data'))
        if 'member' in data:
            self.member = GuildMember(data.get('member'))
        if 'user' in data:
            self.user = User(data.get('user'))

    async def reply(self, response, ephemeral: bool = False):
        if response is None:
            return
        elif type(response) is InteractionResponse:
            return await api_call(f'/interactions/{self.id}/{self.token}/callback', "POST", json=response)
        elif type(response) is str:
            flags = 64 if ephemeral else None
            response: InteractionResponse = {'type': 4, 'data': {'content': response, 'flags': flags}}
            await self.reply(response)

    async def error(self, extra: str = None):
        if extra is not None:
            await self.reply('There was an error executing this command: ' + extra, True)
        else:
            await self.reply('There was an error executing this command.', True)

    async def no_permission(self, extra: Permissions = None):
        if extra is not None:
            await self.reply(f'You need the `{extra.name}` permission to use this.', True)
        else:
            await self.reply('You don\'t have permission to use this.', True)
