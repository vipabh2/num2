import os
import asyncio
from telethon import TelegramClient
from code import *
from top import *
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
ABH = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
async def main():
    print("✅ Bot is running as a bot account (not userbot).")
    await ABH.run_until_disconnected()
asyncio.run(main())
