from telethon import TelegramClient, events
import os
import random

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
client = TelegramClient('new_bot_session', api_id, api_hash).start(bot_token=bot_token)

# قائمة الردود المحتملة
abh = [
    "ها",
    "شرايد",
    "تفظل",
    "قُل",
    "😶"
]


@client.on(events.NewMessage(func=lambda e: e.text and ('مخفي' in e.text.strip().lower() or 'المخفي' in e.text.strip().lower())))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(vipabh, file=vipabh)
    else:
        await event.reply(vipabh)

# تشغيل العميل
client.run_until_disconnected()
