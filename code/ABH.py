import os, asyncio, json, pytz
from telethon import TelegramClient, events
from datetime import datetime
from ABH import *
from database import *
from db import *
timezone = pytz.timezone('Asia/Baghdad')
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
async def main():
    await ABH.start()
    await ABH.run_until_disconnected()
asyncio.run(main())
