from telethon import TelegramClient
from code import *
from top import *
from ABH import *
import os
def main():
    print("config is starting...")
    ABH.start(bot_token=bot_token)
    ABH.run_until_disconnected()
if __name__ == "__main__":
    main()
