from classes.component import *
from classes.interaction import Interaction
from classes.permissions import Permissions
from data_models.interaction import TextInputStyle


async def on_command(interaction: Interaction, client):
    if Permissions.ADMINISTRATOR not in interaction.member.permissions_list:
        await interaction.no_permission_user(Permissions.MANAGE_MESSAGES)
        return
    subcommand = interaction.data.options[0].value
    if subcommand == 'resume':
        await client.reconnect_socket()
        await interaction.reply(f'Attempting to test: "{subcommand}"', True)
    elif subcommand == 'reconnect':
        await client.reconnect_socket(False)
        await interaction.reply(f'Attempting to test: "{subcommand}"', True)
    elif subcommand == 'error':
        await interaction.error()
    elif subcommand == 'modal':
        component = Modal().custom_id('id').title('the wonderful world of space') \
            .add_component(ActionRow().add_component(TextInput('name', TextInputStyle.SHORT, 'name'))) \
            .add_component(
            ActionRow().add_component(TextInput('box', TextInputStyle.PARAGRAPH, label='Type Here')))
        await interaction.reply_modal(component)
    else:
        await interaction.reply(f'Invalid Argument.', True)
