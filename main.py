import asyncio
import json
from http.client import *

import aiohttp
import websockets

from listeners import *

url = "https://discord.com/api/v9"


async def geturl():
    hostname = 'discord.com'
    connection = HTTPSConnection(hostname)
    connection.putrequest('GET', '/api/v9/gateway/bot')
    connection.putheader('Authorization', 'Bot %s' % config['token'])
    connection.endheaders()
    response = connection.getresponse().read().decode()
    url = json.loads(response)['url']
    return url


reconnect = False


async def login():
    here_ws = None
    session_id = ''
    last_sequence = None
    op7 = False
    async with websockets.connect(f'{await geturl()}?v=9&encoding=json') as ws:
        here_ws = ws

        global reconnect
        async for msg in here_ws:
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
                asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval'], last_sequence))
                print(data)
            if data['op'] == 0:
                last_sequence = data['s']
            if data['t'] == 'READY':
                session_id = data['d']['session_id']
                await on_ready(data)
            elif data['t'] == 'MESSAGE_CREATE':
                await on_message_create(data)
            elif data['t'] == 'INTERACTION_CREATE':
                await on_interaction_create(data)
            elif data['op'] == 11:
                print(data)
                pass
            elif data['op'] == 9:
                reconnect = True
            elif data['op'] == 7:
                # TODO fix that stupid reconnecting thing
                print(data)
                op7 = True
                ws = websockets.connect(f'{await geturl()}?v=9&encoding=json')
                reconnect = True
                pass
            else:
                print(data)
    while reconnect:
        here_ws = websockets.connect(f'{await geturl()}?v=9&encoding=json')
        if op7:
            here_ws.send(json.dumps({"op": 6,
                                     "d": {"token": config['token'], "session": session_id, "seq": last_sequence}}))
        reconnect = False


async def heartbeat(ws, interval, last_sequence):
    while True:
        await asyncio.sleep(interval / 1000)
        await ws.send(json.dumps({"op": 1, "d": last_sequence}))


with open('C:/Users/gabri/dev/Discord/prism-field-bot/config.json', encoding='utf-8') as configfile:
    config = json.load(configfile)


async def main():
    # TODO add youtube
    await login()


# async def on_ready():
#     await send_text_msg_channel("822900347810873405", "hi")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
