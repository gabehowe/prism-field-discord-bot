import random

from classes.interaction import Interaction
from classes.member import User
from classes.message import Message
from classes.slashcommandmanager import SlashCommand, SlashCommandManager
from commands import ping, jumbo, purge
from util import send_text_msg_channel

bot: User
command_manager = SlashCommandManager()


async def on_ready(data):
    print(data)
    global bot
    bot = User(data['d']['user'])
    print('Ready!')
    ping_command = SlashCommand()
    ping_command.name = 'ping'
    ping_command.description = 'pings the bot'
    jumbo_command = SlashCommand()
    jumbo_command.name = 'jumbo'
    jumbo_command.description = 'resizes custom emojis'
    jumbo_command.options = [{"name": "emoji", "description": 'the emoji to resize', "type": 3, "required": True}]
    await command_manager.load_commands(bot)
    # cmd = filter(item.name == jumbo_command.name for item in command_manager.commands_array)
    # jumbo_command.id = cmd[0].id
    # await command_manager.modify_command(jumbo_command, bot)
    await command_manager.register_command(jumbo_command, bot)

    await command_manager.register_command(ping_command, bot)


async def on_message_create(data):
    message = Message(data['d'])
    if message.author.id == bot.id:
        return
    if random.randint(0, 1000) == 1:
        await send_text_msg_channel(message.channel_id, "ew " + (
            message.member.nick if message.member.nick is not None else message.author.username))
    if 'owo' in message.content or 'uwu' in message.content:
        if random.randint(0, 9) == 1:
            await send_text_msg_channel(message.channel_id, "There is no shred of that here.")


async def on_interaction_create(data):
    global command_manager
    interaction = Interaction(data.get('d'))
    # TODO add the rest of the commands
    if interaction.data.name == 'ping':
        await ping.on_command(interaction)
    if interaction.data.name == 'jumbo':
        await jumbo.on_command(interaction)
    if interaction.data.name == 'purge':
        await purge.on_command(interaction, bot)
