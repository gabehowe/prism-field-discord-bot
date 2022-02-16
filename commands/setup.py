import json
import os.path
from typing import Dict

import util
from classes.channel import get_channel
from classes.guild import Guild
from classes.interaction import Interaction
from classes.member import GuildMember
from classes.permissions import Permissions
from classes.role import Role
from util import config


async def on_command(interaction: Interaction):
    try:
        if not interaction.is_guild:
            await interaction.reply('This command must be used in a guild.', True)
            return
        if Permissions.ADMINISTRATOR not in interaction.member.permissions_list:
            await interaction.no_permission_user(Permissions.ADMINISTRATOR)
            return
        if Permissions.SEND_MESSAGES not in interaction.bot.permissions_list:
            await interaction.no_permission_bot(Permissions.SEND_MESSAGES)
            return
        subcommand = interaction.data.options[0].name
        if subcommand == 'rules':
            with open(f'{config["dir"]}\\bot_data\\rules.json',
                      encoding='utf-8') as file:
                rules = json.load(file)
                await interaction.channel.send(rules['img'])
                await interaction.channel.send(rules['text'])
                await interaction.reply('Setup successful.', True)
        if subcommand == 'hints':
            with open(f'{config["dir"]}\\bot_data\\hints.json',
                      encoding='utf-8') as file:
                hints = json.load(file)
                await interaction.channel.send(hints['img'])
                await interaction.channel.send(hints['text'])
                await interaction.reply('Setup successful.', True)
        if subcommand == 'roles':
            if Permissions.MANAGE_ROLES not in interaction.bot.permissions_list:
                await interaction.no_permission_bot(Permissions.MANAGE_ROLES)
                return
            with open(f'{config["dir"]}\\bot_data\\roles.json',
                      encoding='utf-8') as file:
                roles = json.load(file)
                await interaction.channel.send(roles)
            await interaction.reply('Setup successful.', True)
        if subcommand == 'membercount':
            if Permissions.MANAGE_CHANNELS not in interaction.bot.permissions_list:
                await interaction.no_permission_bot(Permissions.MANAGE_CHANNELS)
                return
            channel_id = interaction.data.options[0].options[0].value
            channel = await get_channel(channel_id)
            member_count = len(await interaction.guild.list_members(limit=1000))
            await channel.modify_channel(name=f'Member Count: {member_count}')
            if os.path.exists(f'{config["dir"]}\\bot_data\\member_channels.json'):
                current_file: Dict[str, dict] = json.load(open(f'{config["dir"]}\\bot_data\\member_channels.json'))

                with open(f'{config["dir"]}\\bot_data\\member_channels.json', 'w+') as file:
                    if current_file.get(interaction.guild.id) is not None:
                        member_list_obj = current_file.get(interaction.guild_id)
                        member_list_obj["count_channel_id"] = channel_id
                        member_list_obj["member_count"] = member_count
                        current_file[interaction.guild.id] = member_list_obj

                    else:
                        current_file[interaction.guild.id] = {"member_count": member_count,
                                                              "count_channel_id": channel_id}
                    file.write(json.dumps(current_file))

            else:
                with open(f'{config["dir"]}\\bot_data\\member_channels.json', 'x+') as file:
                    member_channels = {
                        interaction.guild.id: {"member_count": member_count, "count_channel_id": channel_id}}
                file.write(json.dumps(member_channels))
            await interaction.reply(f'Initialized member count for {channel.type.name} channel <#{channel_id}>', True)
    except Exception as e:
        if isinstance(e, util.DiscordAPIError):
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        await interaction.error()
        print(e, e.args)


async def on_select_menu(interaction: Interaction):
    try:
        await interaction.ack_component()
        guild = Guild(await util.api_call(f'/guilds/{interaction.guild.id}'))
        role_names = [i.name.lower() for i in guild.roles]
        for i in [i.lower() for i in interaction.data.values]:
            if i not in role_names:
                await interaction.guild.add_role(i.title())
        guild = Guild(await util.api_call(f'/guilds/{interaction.guild.id}'))
        for e in guild.roles:
            if e.name.lower() in interaction.data.values:
                await interaction.member.add_role(e.id, guild.id)
    except Exception as e:
        if isinstance(e, util.DiscordAPIError):
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        await interaction.error()
        print(e, e.args)


async def on_reset_roles(interaction: Interaction):
    try:
        await interaction.ack_component()
        role_names = ['americas', 'not american', 'furry', 'gamer', 'announcements', 'weeb']
        member = GuildMember(
            await util.api_call(f'/guilds/{interaction.guild.id}/members/{interaction.member.user.id}'))
        guild_roles_json = await util.api_call(f'/guilds/{interaction.guild.id}/roles')
        guild_roles = {}
        for i in guild_roles_json:
            guild_roles[i['id']] = (Role(i))

        for i in member.roles:
            role = guild_roles[i.id]
            if role.name.lower() in role_names:
                await member.remove_role(i.id, interaction.guild.id)
    except Exception as e:
        if isinstance(e, util.DiscordAPIError):
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        await interaction.error()
        print(e, e.args)
