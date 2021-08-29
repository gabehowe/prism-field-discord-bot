import asyncio
import json

from classes.client import Client

with open('C:/Users/gabri/dev/Discord/prism-field-bot/config.json', encoding='utf-8') as configfile:
    config = json.load(configfile)


async def main():
    client = Client()

    await client.run(config['token'])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
