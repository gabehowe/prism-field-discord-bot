import datetime

import util
from classes.interaction import Interaction
from classes.member import User
from classes.message import Message
from classes.permissions import Permissions
from util import api_call, DiscordAPIError


async def on_command(interaction: Interaction, bot: User):
    if not hasattr(interaction, 'member'):
        await interaction.reply('This command must be used in a guild.', True)
        return
    if Permissions.MANAGE_MESSAGES not in interaction.member.permissions_list:
        await interaction.no_permission_user(Permissions.MANAGE_MESSAGES)
        return
    bot_member = interaction.bot
    if Permissions.SEND_MESSAGES not in bot_member.permissions_list:
        await interaction.no_permission_bot(Permissions.SEND_MESSAGES)
        return
    if Permissions.MANAGE_MESSAGES not in bot_member.permissions_list:
        await interaction.no_permission_bot(Permissions.MANAGE_MESSAGES)
        return

    try:

        amount = int(interaction.data.options[0].value)
        if amount not in range(1, 101):
            await interaction.reply('amount must be within 1-100', True)
            return

        messages: list = await api_call(f'/channels/{interaction.channel.id}/messages?limit={amount}')
        if type(messages) is not list:
            await interaction.error()
            return
        for i in messages:
            message = await Message(i).async_init(data=i)
            if message.timestamp.date() <= datetime.datetime.now().date() - datetime.timedelta(weeks=2):
                messages.remove(i)

        message_ids = [it['id'] for it in messages]
        if len(messages) == 1:
            await api_call(f'/channels/{interaction.channel.id}/messages/{message_ids[0]}', 'DELETE')
        elif len(messages) > 1:
            json_ids = {'messages': message_ids}
            await api_call(f'/channels/{interaction.channel.id}/messages/bulk-delete', 'POST',
                           json=json_ids)
        elif len(messages) < 1:
            await interaction.error('Not enough messages found to delete ()')
            return
        print(message_ids)

        await interaction.reply(f'{len(message_ids)} message{"s" if len(message_ids) > 1 else ""} deleted.', True)
    except Exception as e:
        if type(e) is DiscordAPIError:
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        await interaction.error()
        print(e, e.args)
