from classes.slashcommandmanager import *


async def on_command(interaction: Interaction):
    response = InteractionResponse()
    response.content = "pong"
    response.ephemeral = True
    await interaction.reply(response)
