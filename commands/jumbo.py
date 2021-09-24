import re

from emoji import UNICODE_EMOJI_ENGLISH

import util
from classes.interaction import Interaction


async def on_command(interaction: Interaction):
    try:
        emoji_str = str(interaction.data.options[0].value)
        if emoji_str in UNICODE_EMOJI_ENGLISH.keys():
            point_list = []
            final_point = ''
            for i in emoji_str:
                point_list.append(hex(ord(i)).removeprefix('0x'))
            for e in range(0, len(point_list)):
                if e == len(point_list) - 1:
                    final_point += point_list[e]
                    break
                final_point += f'{point_list[e]}-'
            await interaction.reply(f'./emojis/{final_point}.png')

            return
        if emoji_str in re.findall(r'^.*[<]+[a]?[:]+.*[:]+\d+>.*', emoji_str):
            is_animated = any(i == emoji_str for i in re.findall(r'[<]+[a]+.*', emoji_str))
            emoji_id = int(re.findall(r'\d+', emoji_str)[0])
            ext = ".gif" if is_animated else ".png"
            await interaction.reply(f'https://cdn.discordapp.com/emojis/{emoji_id}{ext}')
            return
        await interaction.reply('Invalid Emoji.', True)
    except Exception as e:
        if type(e) is util.DiscordAPIError:
            # noinspection PyTypeChecker
            await util.handle_exceptions(e, interaction)
            return
        print(e)
        await interaction.error()
        await util.log(str(e))
