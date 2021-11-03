import asyncio
import json
from collections import Coroutine
from datetime import datetime
from typing import Any, Optional, Dict

import aiohttp
from aiohttp import ClientWebSocketResponse

import util
from classes.channel import TextChannel
from classes.guild import Guild
from classes.member import User
from colors import printc, Color
from listeners import on_ready, on_message_create, on_interaction_create, on_guild_member_add, on_guild_create, \
    on_guild_member_remove
from util import geturl


class Client:
    url = "https://discord.com/api/v9"

    def __init__(self):
        self.reconnect = False
        self.last_sequence = str
        self.session_id = None
        self.resume = False
        self.events_handler: Optional[Coroutine[Any, Any, None]] = None
        self.token = None
        self.heartbeat_handler: Optional[asyncio.Task] = None
        self.guilds: Dict[str, Guild] = {}
        self.bot: Optional[User] = None
        self.socket: Optional[ClientWebSocketResponse] = None
        self.session = aiohttp.ClientSession()

    async def run(self, token: str):
        self.token = token
        await self.login()

    async def handle_events(self):
        try:
            while True:
                msg = await self.socket.receive()
                if msg.type is aiohttp.WSMsgType.TEXT:
                    await self.handle_message(msg.data)
                elif msg.type is aiohttp.WSMsgType.BINARY:
                    await self.handle_message(msg.data)
                elif msg.type is aiohttp.WSMsgType.ERROR:
                    print(f'Error :O {msg}')
                    raise msg.data
                elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
                    print(msg)
                    raise WebSocketClosure
        except (asyncio.TimeoutError, WebSocketClosure):
            await self.reconnect_socket()
            await self.socket.close()

    async def handle_message(self, msg: str):
        channel: Optional[TextChannel]
        data = json.loads(msg)
        if data['op'] == 10:
            await self.socket.send_str(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": 14055,
                    "properties": {},
                    "compress": False,
                    "large_threshold": 250
                }
            }))
            self.heartbeat_handler = asyncio.ensure_future(self.heartbeat(self.socket, data['d']['heartbeat_interval']))
        if data['op'] == 0:
            self.last_sequence = data['s']
        if data['t'] == 'READY':
            await util.log('Ready.')
            self.session_id = data['d']['session_id']
            self.bot = User(data['d']['user'])
            guilds = await util.api_call('/users/@me/guilds')
            for i in guilds:
                guild = Guild(i)
                self.guilds[guild.id] = guild
            await on_ready(self)
        elif data['t'] == 'GUILD_CREATE':
            guild = Guild(data['d'])
            perms = self.guilds[guild.id].permissions
            self.guilds[guild.id] = guild
            self.guilds[guild.id].permissions = perms
            await on_guild_create(data)
        elif data['t'] == 'GUILD_MEMBER_ADD':
            await on_guild_member_add(data)
        elif data['t'] == 'GUILD_MEMBER_REMOVE':
            await on_guild_member_remove(data)
        elif data['t'] == 'MESSAGE_CREATE':
            await on_message_create(data)
        elif data['t'] == 'INTERACTION_CREATE':
            await on_interaction_create(data, self)
        elif data['t'] == 'GUILD_MEMBER_UPDATE':
            pass
        elif data['t'] == 'MESSAGE_UPDATE':
            pass
        elif data['t'] == 'MESSAGE_DELETE':
            pass
        elif data['t'] == 'MESSAGE_REACTION_ADD':
            pass
        elif data['op'] == 11:
            pass
        elif data['op'] == 9:
            await util.log('Session invalidated, reconnecting...')
            printc(Color.WARNING,
                   str(data) + ' ' + str(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'))
            await self.reconnect_socket(False)

        elif data['op'] == 7:
            await util.log('Session invalidated, reconnecting and resuming...')
            printc(Color.WARNING,
                   str(data) + ' ' + str(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'))
            await self.reconnect_socket()
        else:
            print(
                str(data) + ' ' + str(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'))

    async def reconnect_socket(self, resume=True):
        reconnect_str = 'Reconnecting and resuming...' if resume else 'Reconnecting...'
        await util.log(reconnect_str)
        self.reconnect = False
        self.heartbeat_handler.cancel()
        await self.login()
        await util.log('Reconnected.' if not resume else 'Reconnected and resumed.')
        if resume:
            self.resume = False
            await self.socket.send_str(
                json.dumps({"op": 6, "d": {"token": self.token, "session_id": self.session_id,
                                           "seq": self.last_sequence}}))
        await util.log('Reconnected.')

    async def login(self):
        self.socket = await self.session.ws_connect(url=await geturl(self.token))
        self.events_handler = asyncio.create_task(self.handle_events())
        await self.events_handler

    async def heartbeat(self, ws, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            await ws.send_str(json.dumps({"op": 1, "d": self.last_sequence}))

    async def update_presence(self, presence):
        activities = [{'name': i.name, 'type': i.type} for i in presence.activities]
        await self.socket.send_str(json.dumps({'op': 3, 'd': {'since': presence.since, 'activities': activities,
                                                              'status': presence.status, 'afk': presence.afk}}))


class WebSocketClosure(Exception):
    pass
