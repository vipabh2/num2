from telethon import events ,TelegramClient
import os
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
ABH = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
from telethon.tl.types import MessageEntityUrl
from telethon import events, Button
from ABH import ABH  # type:ignore
from Resources import *
import asyncio
from telethon import events, types
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import InputPeerUser, ReactionEmoji

@ABH.on(events.NewMessage(pattern='ها'))
async def react_to_message(event):
    await ABH(SendReactionRequest(
        peer=event.chat_id,
        msg_id=event.id,
        reaction=[ReactionEmoji(emoticon='❤️')],
        big=True
    ))
