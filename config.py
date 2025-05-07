import os
from telethon import TelegramClient
from code import *
from top import *
from ABH import *
def main():
    print("✅ Bot is starting...")
    ABH.start(bot_token=bot_token)
    ABH.run_until_disconnected()
if __name__ == "__main__":
    main()
