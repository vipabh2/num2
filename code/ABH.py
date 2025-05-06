import os, asyncio, json, pytz
from telethon import TelegramClient, events
from datetime import datetime
from code import *
timezone = pytz.timezone('Asia/Baghdad')
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
hint_gid = -1002168230471
bot = "Anymous"
wfffp = 1910015590
now = datetime.now()
hour = now.strftime("%y\\%m\\%d--%I:%M%p")
اسم_الملف = "التشغيل.json"
if not os.path.exists(اسم_الملف):
    وقت_التشغيل = hour
    with open(اسم_الملف, "w", encoding="utf-8") as ملف:
        json.dump(وقت_التشغيل, ملف, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern='وقت التشغيل'))
async def time_run(event):
    if event.sender_id == wfffp:
        with open(اسم_الملف, "r", encoding="utf-8") as ملف:
            وقت_التشغيل = json.load(ملف)
        await event.reply(f"وقت التشغيل هو: {وقت_التشغيل}")
hour = now.strftime("%I:%M %p")
print(f'anymous is working at {hour} ✓')
async def main():
    try:
        await ABH.start(bot_token=bot_token)
        await ABH.run_until_disconnected()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await ABH.disconnect()
