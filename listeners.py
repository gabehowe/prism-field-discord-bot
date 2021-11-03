import json
import os
import random

import util
from classes.channel import get_channel
from classes.guild import Guild
from classes.interaction import Interaction
from classes.member import User, GuildMember
from classes.message import Message
from classes.presence import Presence, Activity
from classes.slashcommandmanager import SlashCommandManager
from colors import printc, Color
from commands import ping, jumbo, purge, setup, test
from data_models.interaction import InteractionType
from data_models.presence import Status, ActivityType
from util import log

bot: User
command_manager = SlashCommandManager()


async def on_ready(client):
    global bot
    bot = client.bot
    activity = Activity({'name': 'AntiPrism Vlogs on Youtube', 'type': ActivityType.WATCHING,
                         'url': 'https://www.youtube.com/channel/UClmGXpXQnF5P7h3YxcYl_wQ?'})
    presence = Presence({'since': None, 'status': Status.ONLINE, 'afk': False, 'activities': [activity]})
    await client.update_presence(presence)
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


async def on_guild_member_add(data):
    member = GuildMember(data['d'])
    if not os.path.exists(f'{util.config["dir"]}\\bot_data\\member_channels.json'):
        with open('bot_data/member_channels.json', 'x+') as new_file:
            new_file.write('{}')
    with open('bot_data/member_channels.json', 'r+') as file:
        json_file: dict = json.load(file)
        if json_file.get(member.guild_id) is not None:
            json_file[member.guild_id]['member_count'] += 1
            channel_id = json_file[member.guild_id]['count_channel_id']
            channel = await get_channel(channel_id)
            if channel is not None:
                await channel.modify_channel(name=f'Member Count: {json_file[member.guild_id]["member_count"]}')
    with open('bot_data/member_channels.json', 'w+') as file:
        file.write(json.dumps(json_file))


async def on_guild_create(data):
    guild = Guild(data['d'])
    if not os.path.exists(f'{util.config["dir"]}\\bot_data\\member_channels.json'):
        with open('bot_data/member_channels.json', 'x+') as new_file:
            new_file.write('{}')
    with open('bot_data/member_channels.json', 'r+') as file:
        json_file: dict = json.load(file)
        if json_file.get(guild.id) is not None:
            json_file[guild.id]['member_count'] = guild.member_count
            channel_id = json_file[guild.id]['count_channel_id']
            channel = await get_channel(channel_id)
            if channel is not None:
                await channel.modify_channel(name=f'Member Count: {json_file[guild.id]["member_count"]}')
    with open('bot_data/member_channels.json', 'w+') as file:
        file.write(json.dumps(json_file))


async def on_guild_member_remove(data):
    member = GuildMember(data['d'])
    if not os.path.exists(f'{util.config["dir"]}\\bot_data\\member_channels.json'):
        with open('bot_data/member_channels.json', 'x+') as new_file:
            new_file.write('{}')
    with open('bot_data/member_channels.json', 'r+') as file:
        json_file: dict = json.load(file)
        if json_file.get(member.guild_id) is not None:
            json_file[member.guild_id]['member_count'] -= 1
            channel_id = json_file[member.guild_id]['count_channel_id']
            channel = await get_channel(channel_id)
            if channel is not None:
                await channel.modify_channel(name=f'Member Count: {json_file[member.guild_id]["member_count"]}')
    with open('bot_data/member_channels.json', 'w+') as file:
        file.write(json.dumps(json_file))


class StopCommandException(BaseException):
    def __init__(self):
        printc(Color.RED, '!!stop!! used! terminating')
