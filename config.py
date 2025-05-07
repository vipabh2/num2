import os
import asyncio
from code import *
from top import *
async def main():
    print("✅ Bot is running as a bot account (not userbot).")
    await ABH.run_until_disconnected()
asyncio.run(main())
