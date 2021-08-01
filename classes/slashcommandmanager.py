import warnings

from classes.member import User
from util import api_call


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


class ApplicationCommandData:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.resolved = data.get('resolved')
        self.options = data.get('options')
        self.custom_id = data.get('custom_id')
        self.component_type = data.get('component_type')


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