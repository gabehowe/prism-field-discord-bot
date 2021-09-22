import argparse
import asyncio
import json

import websockets

from classes.member import User
from classes.slashcommandmanager import load_command, SlashCommandManager
from util import geturl, api_call

parser = argparse.ArgumentParser(description='updates slash command data')
parser.add_argument('--file', help='the JSON file to send. if GET is used, the file to save the data to', required=True)
parser.add_argument('--guild_id', help='the id of the guild to modify the command for (leave empty for global)',
                    default=None)
parser.add_argument('--method', help='POST, PATCH, DELETE, or GET', required=True,
                    choices=['POST', 'PATCH', 'DELETE', 'GET'])
parser.add_argument('--cmd_id', help='command id used for patch')


async def login_here():
    async with websockets.connect(f'{await geturl(config["token"])}?v=9&encoding=json') as ws:
        async for msg in ws:
            data = json.loads(msg)
            if data['op'] == 10:
                await ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": config['token'],
                        "intents": 14055,
                        "properties": {},
                        "compress": False,
                        "large_threshold": 250
                    }
                }))
            if data['t'] == 'READY':
                await run_ready(data)
            elif data['op'] == 11:
                pass
            else:
                print(data)


with open('C:/Users/gabri/dev/Discord/prism-field-bot-server/config.json', encoding='utf-8') as configfile:
    config = json.load(configfile)


async def run_ready(data):
    args = parser.parse_args()
    is_guild = False if args.guild_id is None else True
    bot = User(data['d']['user'])
    file = json.loads(open(args.file).read())

    method = args.method

    if is_guild:
        if method == 'DELETE':
            json_object = await api_call(f'/applications/{bot.id}/guilds/{str(args.guild_id)}/commands/{args.cmd_id}',
                                         method)
            print(json_object)
        elif method == 'PATCH':
            json_object = await api_call(f'/applications/{bot.id}/guilds/{str(args.guild_id)}/commands/{args.cmd_id}',
                                         method, json=file)
            print(json_object)
        elif method == 'GET':
            json_object = await api_call(f'/applications/{bot.id}/guilds/{str(args.guild_id)}/commands/{args.cmd_id}',
                                         method)
            print(json_object)
            with open(args.file, 'w+x') as e:
                e.write(json_object)
        elif method == 'POST':
            json_object = await api_call(f'/applications/{bot.id}/guilds/{str(args.guild_id)}/commands',
                                         method, json=file)
            print(json_object)
    else:
        if method == 'DELETE':
            json_object = await api_call(f'/applications/{bot.id}/commands/{args.cmd_id}',
                                         method)
            print(json_object)
        elif method == 'PATCH':
            json_object = await api_call(f'/applications/{bot.id}/commands/{args.cmd_id}',
                                         method, json=file)
            print(json_object)
        elif method == 'GET':
            json_object = await api_call(f'/applications/{bot.id}/commands/{args.cmd_id}',
                                         method)
            print(json_object)
            with open(args.file, 'w+x') as e:
                e.write(json_object)
        elif method == 'POST':
            cmd = await load_command(file)

            print(await SlashCommandManager().register_command(cmd, bot))


asyncio.get_event_loop().run_until_complete(login_here())
