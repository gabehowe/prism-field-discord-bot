import datetime
import json
from re import findall

import pytz

from classes.member import User, GuildMember, load_guild_member
from classes.message import load_message, Message
from util import api_call, DiscordAPIError


async def on_command(interaction, bot : User):
    try:
        if interaction.channel_id is None:
            await interaction.reply_text('This command must be used in a guild', True)
            return

        amount = int(interaction.data.options[0]['value'])
        # bot_member_call = await api_call(f'/guilds/{interaction.guild_id}/members/{bot.id}')
        # bot_member = await load_guild_member(bot_member_call)
        # if bot_member.permissions
        if amount not in range(2, 100):
            await interaction.reply_text('amount must be within 2-100', True)
            return

        messages = await api_call(f'/channels/{interaction.channel_id}/messages?limit={amount}')  # type: list
        if type(messages) is not list:
            await interaction.error()
            return
        for i in messages:
            message = await load_message(i)  # type: Message
            if message.timestamp.replace(tzinfo=pytz.UTC) < datetime.datetime.utcnow().replace(
                    tzinfo=pytz.UTC) - datetime.timedelta(weeks=2):
                messages.remove(i)

        message_ids = [it['id'] for it in messages]

        json_ids = {'messages': message_ids}
        call = await api_call(f'/channels/{interaction.channel_id}/messages/bulk-delete', 'POST',
                              json=json_ids)
        print()
        await interaction.reply_text(f'{amount} messages deleted.')
    except Exception as e:
        code = int(findall(r'\d+', str(e))[0])
        if code == 50013:
            await interaction.error('Missing Permissions')
        else:
            await interaction.error()
            print(e, e.args)
