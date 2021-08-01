import warnings

from classes.member import User, load_guild_member, load_user
from util import api_call


class InteractionResponse:
    def __init__(self):
        self.type = 4
        self.tts = None
        self.content = None
        self.embeds = None
        self.components = None
        self.ephemeral = False
        self.allowed_mentions = None


class SlashCommand:
    def __init__(self):
        self.name = None
        self.description = None
        self.options = None
        self.default_permission = None
        self.id = None
        self.guild_id = None
        self.application_id = None


async def load_command(data: dict):
    cmd = SlashCommand()
    cmd.id = data.get('id')
    cmd.application_id = data.get('application_id')
    cmd.guild_id = data.get('guild_id')
    cmd.name = data.get('name')
    cmd.description = data.get('description')
    cmd.options = data.get('options')
    cmd.default_permission = data.get('default_permission')
    return cmd


class Interaction:
    def __init__(self):
        self.id = None
        self.application_id = None
        self.type = None
        self.data = None
        self.guild_id = None
        self.channel_id = None
        self.member = None
        self.user = None
        self.token = None
        self.version = None
        self.message = None

    async def reply_text(self, text: str, ephemeral: bool = False):
        response = InteractionResponse()
        response.content = text
        if ephemeral:
            flags = 64
        else:
            flags = None
        cmd_json = {'type': response.type, 'data': {'flags': flags, 'tts': response.tts, 'embeds': response.embeds,
                                                    'allowed_mentions': response.allowed_mentions,
                                                    'content': response.content,
                                                    'components': response.components}}
        await api_call(f'/interactions/{self.id}/{self.token}/callback', "POST", json=cmd_json)

    async def reply(self, response: InteractionResponse):
        if response.ephemeral:
            flags = 64
        else:
            flags = None
        cmd_json = {'type': response.type, 'data': {'tts': response.tts, 'embeds': response.embeds,
                                                    'allowed_mentions': response.allowed_mentions,
                                                    'flags': flags, 'content': response.content,
                                                    'components': response.components}}
        await api_call(f'/interactions/{self.id}/{self.token}/callback', "POST", json=cmd_json)

    async def error(self, extra: str = None):
        if extra is not None:
            await self.reply_text('There was an error executing this command: ' + extra, True)
        else:
            await self.reply_text('There was an error executing this command.', True)


async def load_interaction(data: dict):
    interaction = Interaction()
    interaction.id = data.get('id')
    interaction.application_id = data.get('application_id')
    interaction.type = data.get('type')
    if data.get('data') is not None:
        interaction.data = await load_application_command_data(data.get('data'))
    else:
        interaction.data = None
    interaction.guild_id = data.get('guild_id')
    interaction.channel_id = data.get('channel_id')
    if data.get('member') is None:
        interaction.member = None
    else:
        interaction.member = await load_guild_member(data.get('member'))
    if data.get('user') is None:
        interaction.user = None
    else:
        interaction.user = await load_user(data.get('user'))
    interaction.token = data.get('token')
    interaction.version = data.get('version')
    interaction.message = data.get('message')
    return interaction


class ApplicationCommandData:
    def __init__(self):
        self.id = None
        self.name = None
        self.resolved = None
        self.options = None
        self.custom_id = None
        self.component_type = None


async def load_application_command_data(data: dict):
    it = ApplicationCommandData()
    it.id = data.get('id')
    it.name = data.get('name')
    it.resolved = data.get('resolved')
    it.options = data.get('options')
    it.custom_id = data.get('custom_id')
    it.component_type = data.get('component_type')

    return it


class SlashCommandManager:
    def __init__(self):
        self.commands_array = []
        self.loaded = False

    async def load_commands(self, bot):

        commands_object = await api_call(f"/applications/{bot.id}/commands")
        for i in commands_object:
            self.commands_array.append(await load_command(i))
        self.loaded = True

    async def register_command(self, slash_command: SlashCommand, bot: User):
        json_command = {"name": slash_command.name, "description": slash_command.description,
                        "options": slash_command.options, "default_permission": slash_command.default_permission}
        if any(i.name == json_command['name'] for i in self.commands_array):
            return
        command = await api_call(f"/applications/{bot.id}/commands", "POST", json=json_command)

        self.commands_array.append(command)
        return command

    async def modify_command(self, slash_command: SlashCommand, bot: User):
        if slash_command.id is None:
            warnings.warn('slash command has no id')
            return
        json_command = {"name": slash_command.name, "description": slash_command.description,
                        "options": slash_command.options, "default_permission": slash_command.default_permission}
        if any(i.name == json_command['name'] for i in self.commands_array):
            return

        command = await api_call(f"/applications/{bot.id}/commands/{slash_command.id}", "PATCH", json=json_command)

        self.commands_array.append(command)
        return command
