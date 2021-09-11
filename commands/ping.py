import util
from classes.interaction import Interaction
from util import DiscordAPIError


async def on_command(interaction: Interaction):
    try:
        await interaction.reply('pong', True)
    except Exception as e:
        if type(e) is DiscordAPIError:
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        await interaction.error()
        print(e, e.args)
