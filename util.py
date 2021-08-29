import datetime
import json
from http.client import HTTPSConnection
from typing import Optional

import aiohttp

url = "https://discord.com/api/v9"
with open('C:/Users/gabri/dev/Discord/prism-field-bot/config.json', encoding='utf-8') as configfile:
    config = json.load(configfile)


async def send_text_msg_channel(channel_id, content):
    return await api_call(f'/channels/{channel_id}/messages', "POST", json={"content": content})


async def api_call(path, method="GET", **kwargs):
    defaults = {"headers": {"Authorization": f'Bot {config["token"]}',
                            "User-Agent": "dBot (https://github.com/gabehowe, 0.1.0)",
                            "Content-Type": "application/json"}}
    kwargs = dict(defaults, **kwargs)
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url + path, **kwargs) as response:
            try:
                assert 200 == response.status, response.reason
            except AssertionError:
                pass

            json_response = await response.json(content_type=response.content_type)
            if json_response is not None:
                if 'message' in json_response:
                    raise DiscordAPIError(str(f"Error: {str(json_response['message'])} {str(json_response['code'])}"))

        return json_response


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
        return datetime.datetime.fromisoformat(time)
    return None


class DiscordAPIError(Exception):
    pass
