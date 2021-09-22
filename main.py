import asyncio
import json
import os
import sys

import listeners
import util
from classes.client import Client
from colors import Color, printc

with open('C:/Users/gabri/dev/Discord/prism-field-bot/config.json', encoding='utf-8') as configfile:
    config = json.load(configfile)


async def main():
    while True:
        try:
            client = Client()
            await client.run(config['token'])
        except Exception as e:
            if isinstance(e, listeners.StopCommandException):
                raise
            # raise
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_str = f'Encountered an error: `{e.__class__.__name__}: {exc_obj}` at `{file_name}:{exc_tb.tb_lineno}`'
            await util.log(err_str)
            printc(Color.RED, err_str)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except BaseException as ex:
    asyncio.get_event_loop().run_until_complete(util.log('Exited.'))
    print('exited')
    raise
