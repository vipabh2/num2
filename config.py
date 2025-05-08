from ABH import ABH, events, bot_token
from datetime import datetime
import os, json, pytz
from Resources import * 
from addanddel import * 
from Program import * 
from count import *
from games import * 
from group import * 
from guard import * 
from reply import * 
from mem import * 
from top import * 
now = datetime.now()
hour = now.strftime("%y\\%m\\%d--%I:%M%p")
اسم_الملف = "التشغيل.json"
if not os.path.exists(اسم_الملف):
    وقت_التشغيل = hour
    with open(اسم_الملف, "w", encoding="utf-8") as ملف:
        json.dump(وقت_التشغيل, ملف, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern='وقت التشغيل'))
async def time_run(event):
    if event.sender_id==wfffp:
        try:
            with open(اسم_الملف,"r",encoding="utf-8") as ملف:
                وقت_التشغيل=json.load(ملف)
            baghdad_tz=pytz.timezone("Asia/Baghdad")
            الآن=datetime.now(baghdad_tz)
            الساعة=الآن.strftime("%I:%M %p")
            الرسالة=f"🕒 وقت التشغيل: {وقت_التشغيل}\n🕰️ الوقت الحالي في بغداد: {الساعة}"
            await event.reply(الرسالة)
        except Exception as e:
            await event.reply(f"خطأ: {str(e)}")
print(f'anymous is working at {hour} ✓')
def main():
    print("config is starting...")
    ABH.start(bot_token=bot_token)
    ABH.run_until_disconnected()
if __name__ == "__main__":
    main()
