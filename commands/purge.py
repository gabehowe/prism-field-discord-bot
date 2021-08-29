import datetime
from re import findall

import pytz

from classes.interaction import Interaction
from classes.member import User
from classes.message import Message
from util import api_call
from classes.permissions import Permissions


async def on_command(interaction: Interaction, bot: User):
    if not hasattr(interaction, 'member'):
        await interaction.reply('This command must be used in a guild.', True)
        return
    if Permissions.MANAGE_MESSAGES not in interaction.member.permissions_list:
        await interaction.no_permission(Permissions.MANAGE_MESSAGES)
        return

    try:

        amount = int(interaction.data.options[0]['value'])
        # bot_member_call = await api_call(f'/guilds/{interaction.guild_id}/members/{bot.id}')
        # bot_member = await load_guild_member(bot_member_call)
        # if bot_member.permissions
        if amount not in range(1, 101):
            await interaction.reply('amount must be within 1-100', True)
            return

        messages = await api_call(f'/channels/{interaction.channel_id}/messages?limit={amount}')  # type: list
        if type(messages) is not list:
            await interaction.error()
            return
        for i in messages:
            message = Message(i)  # type: Message
            if message.timestamp.date() <= datetime.datetime.now().date() - datetime.timedelta(weeks=2):
                messages.remove(i)

        message_ids = [it['id'] for it in messages]
        if len(messages) == 1:
            await api_call(f'/channels/{interaction.channel_id}/messages/{message_ids[0]}', 'DELETE')
        elif len(messages) > 1:
            json_ids = {'messages': message_ids}
            await api_call(f'/channels/{interaction.channel_id}/messages/bulk-delete', 'POST',
                           json=json_ids)
        elif len(messages) < 1:
            await interaction.error('Not enough messages found to delete ()')
            return
        print(message_ids)

        await interaction.reply(f'{len(message_ids)} message{"s" if len(message_ids) > 1 else ""} deleted.', True)
    except Exception as e:
        code = int(findall(r'\d+', str(e))[0])
        if code == 50034:
            await interaction.error('M')
        await interaction.error()
        print(e, e.args)
