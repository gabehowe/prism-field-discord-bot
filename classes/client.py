import asyncio
import json
from http.client import HTTPSConnection
from typing import Any
from collections import Coroutine

import websockets
from websockets.exceptions import ConnectionClosedError

from listeners import on_ready, on_message_create, on_interaction_create
from util import geturl


class Client:
    url = "https://discord.com/api/v9"

    def __init__(self):
        self.reconnect = False
        self.last_sequence = str
        self.session_id = None
        self.resume = False
        self.events_handler = None  # type: Coroutine[Any,Any,None] | None
        self.token = None
        self.heartbeat_handler = None

    async def run(self, token: str):
        self.token = token
        await self.login()

    async def handle_events(self, ws):
        try:
            async for msg in ws:
                data = json.loads(msg)
                if data['op'] == 10:
                    await ws.send(json.dumps({
                        "op": 2,
                        "d": {
                            "token": self.token,
                            "intents": 14055,
                            "properties": {},
                            "compress": False,
                            "large_threshold": 250
                        }
                    }))
                    self.heartbeat_handler = asyncio.ensure_future(self.heartbeat(ws, data['d']['heartbeat_interval']))
                    print(data)
                if data['op'] == 0:
                    self.last_sequence = data['s']
                if data['t'] == 'READY':
                    self.session_id = data['d']['session_id']
                    await on_ready(data)
                elif data['t'] == 'MESSAGE_CREATE':
                    await on_message_create(data)
                elif data['t'] == 'INTERACTION_CREATE':
                    await on_interaction_create(data)
                elif data['op'] == 11:
                    print(data)
                    pass
                elif data['op'] == 9:
                    print(data)
                    self.reconnect = True
                    await ws.close()
                elif data['op'] == 7:
                    print(data)
                    self.resume = True
                    await ws.close()
                else:
                    print(data)
        except ConnectionClosedError:
            self.resume = True

    async def _check_for_reconnect(self):
        while True:
            if self.resume:
                self.resume = False
                self.events_handler.cancel()
                self.heartbeat_handler.cancel()
                async with websockets.connect(f'{await geturl(self.token)}') as ws:
                    self.events_handler = asyncio.create_task(self.handle_events(ws))
                    await self.events_handler
                    await ws.send(json.dumps({"op": 6, "d": {"token": self.token, "session_id": self.session_id,
                                                             "seq": self.last_sequence}}))

            elif self.reconnect:
                self.reconnect = False
                self.events_handler.cancel()
                self.heartbeat_handler.cancel()
                async with websockets.connect(f'{await geturl(self.token)}') as ws:
                    self.events_handler = asyncio.create_task(self.handle_events(ws))
                    await self.events_handler

    async def login(self):
        async with websockets.connect(f'{await geturl(self.token)}?v=9&encoding=json') as ws:
            self.events_handler = asyncio.create_task(self.handle_events(ws))
            await self.events_handler
            await self._check_for_reconnect()

    async def heartbeat(self, ws, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            await ws.send(json.dumps({"op": 1, "d": self.last_sequence}))
