from telethon import events
from code import *
from top import *
import asyncio
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
async def main():
    await ABH.start()
    print("config is running")
    await ABH.run_until_disconnected()
asyncio.run(main())
