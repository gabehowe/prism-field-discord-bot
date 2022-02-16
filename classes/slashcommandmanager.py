import warnings
from typing import Optional, List

from classes.component import Component, ActionRow, Button, SelectMenu, TextInput
from classes.member import User
from data_models.interaction import ApplicationCommandInteractionData, ApplicationCommandInteractionDataOption
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
    def __init__(self, data: ApplicationCommandInteractionData):
        self.id = data.get('id')
        self.name = data.get('name')
        self.resolved = data.get('resolved')
        if 'options' in data:
            self.options = [ApplicationCommandDataOption(i) for i in data.get('options')]
        self.custom_id = data.get('custom_id')
        self.component_type = data.get('component_type')
        self.values: Optional[List[str]] = data.get('values')
        self.components: Optional[List[Component]] = []
        if 'components' in data:
            for i in data.get('components'):
                if i.get('type') == 1:  # 1 is Action Row
                    row = ActionRow()
                    for e in i.get('components'):
                        component = None
                        if e.get('type') == 2:
                            component = Button('blorby', 1).from_json(e)
                        elif e.get('type') == 3:
                            component = SelectMenu('ahwo').from_json(e)
                        elif e.get('type') == 4:
                            component = TextInput('apghaw').from_json(e)
                        row.add_component(component)
                    self.components.append(row)


class ApplicationCommandDataOption:
    def __init__(self, data: ApplicationCommandInteractionDataOption):
        self.name = data.get('name')
        self.type = data.get('type')
        self.value = data.get('value')
        if 'options' in data:
            self.options = [ApplicationCommandDataOption(i) for i in data.get('options')]


class SlashCommandManager:
    def __init__(self):
        self.commands_array: List[SlashCommand] = []
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
