import random

import util
from classes.interaction import Interaction
from classes.member import User
from classes.message import Message
from classes.slashcommandmanager import SlashCommandManager
from colors import printc, Color
from commands import ping, jumbo, purge, setup, test
from data_models.interaction import InteractionType
from util import log

bot: User
command_manager = SlashCommandManager()


async def on_ready(client):
    global bot
    bot = client.bot
    printc(Color.GREEN, 'Ready!')
    await command_manager.load_commands(bot)
    with open('commands.txt', 'w+') as commands_file:
        commands_file.write(str([f'{it.id}, {it.name}, {it.options}\n' for it in command_manager.commands_array]))
    commands_file.close()


async def on_message_create(data):
    message = Message(data['d'])
    await message.async_init(data['d'])
    if message.author.id == bot.id:
        return
    if random.randint(0, 1000) == 1:
        await message.channel.send("ew " + (
            message.member.nick if message.member.nick is not None else message.author.username))
    if 'owo' in message.content.lower() or 'uwu' in message.content.lower():
        if random.randint(1, 5) == 1:
            await message.channel.send("There is no shred of that here.")
    if '!!stop!!' in message.content and message.author.id in util.config.get('stop_perms'):
        raise StopCommandException


async def on_interaction_create(data, client):
    global command_manager
    interaction = await Interaction(data.get('d')).async_init(data.get('d'), client)
    await log(
        f'{interaction.user.username} used "{interaction.data.name or interaction.data.custom_id}".')
    # TODO add the rest of the commands
    if interaction.type == InteractionType.APPLICATION_COMMAND:
        if interaction.data.name == 'ping':
            await ping.on_command(interaction)
        elif interaction.data.name == 'jumbo':
            await jumbo.on_command(interaction)
        elif interaction.data.name == 'purge':
            await purge.on_command(interaction, bot)
        elif interaction.data.name == 'setup':
            await setup.on_command(interaction)
        elif interaction.data.name == 'test':
            await test.on_command(interaction, client)

    if interaction.type == InteractionType.MESSAGE_COMPONENT:
        if interaction.data.custom_id == 'roles_select':
            await setup.on_select_menu(interaction)
        if interaction.data.custom_id == 'reset_roles':
            await setup.on_reset_roles(interaction)


class StopCommandException(BaseException):
    def __init__(self):
        printc(Color.RED, '!!stop!! used! terminating')
