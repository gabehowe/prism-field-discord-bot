from classes.interaction import Interaction
from classes.permissions import Permissions


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
    else:
        await interaction.reply(f'Invalid.', True)
