from classes.interaction import InteractionResponse, Interaction
from classes.slashcommandmanager import *


async def on_command(interaction: Interaction):
    await interaction.reply_text('pong', True)
