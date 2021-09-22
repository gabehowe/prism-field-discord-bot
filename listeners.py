import random

from classes.interaction import Interaction
from classes.member import User
from classes.message import Message
from classes.slashcommandmanager import SlashCommandManager
from commands import ping, jumbo, purge, setup
from data_models.interaction import InteractionType
from util import log

bot: User
command_manager = SlashCommandManager()


async def on_ready(data, client):
    print(data)
    global bot
    bot = client.bot
    print('Ready!')
    await command_manager.load_commands(bot)


async def on_message_create(data):
    message = Message(data['d'])
    await message.async_init(data['d'])
    if message.author.id == bot.id:
        return
    if random.randint(0, 1000) == 1:
        await message.channel.send("ew " + (
            message.member.nick if message.member.nick is not None else message.author.username))
    if 'owo' in message.content or 'uwu' in message.content:
        if random.randint(0, 9) == 1:
            await message.channel.send("There is no shred of that here.")


async def on_interaction_create(data, client):
    global command_manager
    interaction = await Interaction(data.get('d')).async_init(data.get('d'), client)
    await log(f'{interaction.member.user.username} used "{interaction.data.name or interaction.data.custom_id}".')
    # TODO add the rest of the commands
    if interaction.type == InteractionType.APPLICATION_COMMAND:
        if interaction.data.name == 'ping':
            await ping.on_command(interaction)
        if interaction.data.name == 'jumbo':
            await jumbo.on_command(interaction)
        if interaction.data.name == 'purge':
            await purge.on_command(interaction, bot)
        if interaction.data.name == 'setup':
            await setup.on_command(interaction)
        if interaction.data.name == 'test':
            subcommand = interaction.data.options[0].name
            if subcommand == 'resume':
                await client.reconnect_socket()
            elif subcommand == 'reconnect':
                await client.reconnect_socket(False)

    if interaction.type == InteractionType.MESSAGE_COMPONENT:
        if interaction.data.custom_id == 'roles_select':
            await setup.on_select_menu(interaction)
        if interaction.data.custom_id == 'reset_roles':
            await setup.on_reset_roles(interaction)
