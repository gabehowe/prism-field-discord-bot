import asyncio
import json
import math
from datetime import datetime
from http.client import HTTPSConnection
from typing import Optional

import aiohttp
import requests
from aiohttp import client_exceptions

from colors import printc, Color
from data_models.channel import ChannelType

url = "https://discord.com/api/v9"
config: dict


def _update_config():
    global config
    with open('./config.json', encoding='utf-8') as configfile:
        config = json.load(configfile)


_update_config()


async def log(string: str):
    channel_json = await api_call(f'/channels/{config["log_channel_id"]}')

    if channel_json.get('type') in [ChannelType.GUILD_TEXT, ChannelType.DM, ChannelType.GROUP_DM,
                                    ChannelType.GUILD_NEWS,
                                    ChannelType.GUILD_STORE, ChannelType.GUILD_PUBLIC_THREAD,
                                    ChannelType.GUILD_PRIVATE_THREAD]:
        _update_config()
        log_id = config['log_channel_id']
        try:
            return await api_call(f'/channels/{log_id}/messages', "POST", json={"content": str(
                f'[<t:{math.floor(datetime.now().timestamp())}:D><t:{math.floor(datetime.now().timestamp())}:T>] {string}')})
        except DiscordAPIError as e:
            if e.code == 50013:
                printc(Color.RED, "Missing Permissions")
            else:
                raise


async def api_call(path, method="GET", **kwargs):
    _update_config()
    defaults = {"headers": {"Authorization": f'Bot {config["token"]}',
                            "User-Agent": "dBot (https://github.com/gabehowe, 0.1.0)",
                            "Content-Type": "application/json"}}
    kwargs = dict(defaults, **kwargs)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url + path, **kwargs) as response:
                try:
                    assert 200 == response.status, response.reason
                except AssertionError:
                    pass

                json_response = await response.json(content_type=response.content_type)
                if json_response is not None:
                    if 'retry_after' in json_response:
                        await asyncio.sleep(json_response['retry_after'])
                        return
                    if 'message' in json_response:
                        if json_response.get('code') == 10003:
                            return None
                        print(json_response)
                        raise DiscordAPIError(json_response.get('code'), json_response.get('message'))

            return json_response
    except client_exceptions.ClientConnectorError:
        printc(Color.RED, 'ClientConnectorError (Probably caused by lack of internet connection).')
        pass


async def geturl(token: str):
    hostname = 'discord.com'
    connection = HTTPSConnection(hostname)
    connection.putrequest('GET', '/api/v9/gateway/bot')
    connection.putheader('Authorization', 'Bot %s' % token)
    connection.endheaders()
    response = connection.getresponse().read().decode()
    return json.loads(response)['url']


def parse_time(time: Optional[str]):
    if time:
        return datetime.fromisoformat(time)
    return None


class DiscordAPIError(Exception):
    def __init__(self, code, message, body=None):
        self.code = code
        self.message = message
        self.body = body

    pass


async def handle_exceptions(e: DiscordAPIError, interaction):
    code = e.code
    if code == 50013:
        await interaction.no_permission_bot()
        return
    else:
        print(f'DiscordAPIError: {e}')
        await log(str(e))


def sync_api_call(path, method="GET", **kwargs):
    defaults = {"headers": {"Authorization": f'Bot {config["token"]}',
                            "User-Agent": "dBot (https://github.com/gabehowe, 0.1.0)",
                            "Content-Type": "application/json"}}
    kwargs = dict(defaults, **kwargs)
    response = requests.request(method, url + path, **kwargs)
    try:
        assert 200 == response.status_code, response.reason
    except AssertionError:
        pass

    json_response = response.json()
    print(json_response)
    if json_response is not None:
        if 'retry_after' in json_response:
            return
        if 'message' in json_response:
            print(json_response)
            raise DiscordAPIError(json_response.get('code'), json_response.get('message'))

    return json_response
