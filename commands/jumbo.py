import re

from classes.interaction import Interaction


async def on_command(interaction: Interaction):
    try:
        emoji_str = str(interaction.data.options[0]['value'])
        if emoji_str not in re.findall(r'^.*[<]+[a]?[:]+.*[:]+\d+>.*$', emoji_str):
            await interaction.reply("Invalid Emoji (Emoji must be custom)")
            return
        is_animated = any(i == emoji_str for i in re.findall(r'[<]+[a]+.*', emoji_str))
        emoji_id = int(re.findall(r'\d+', emoji_str)[0])
        ext = ".gif" if is_animated else ".png"
        await interaction.reply(f'https://cdn.discordapp.com/emojis/{emoji_id}{ext}')
    except Exception as e:
        await interaction.error()
        print(e)
