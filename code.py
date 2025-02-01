from telethon import TelegramClient, events
import os, random 

# تحميل بيانات API
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='/start'))
async def reply_abh(event):
    if event.is_private:  # إذا كان المستخدم يرسل في الدردشة الخاصة
        await event.reply("👋 أهلاً! استخدم هذا البوت داخل المجموعة فقط.")
        return

    # 🔹 يعمل الآن في جميع المجموعات بدون قيود على chat_id
    iu = random.choice(["ch1", "ch2"])  

    if iu == "ch1":  
        rl = random.randint(1222, 1223)
        url = f"https://t.me/VIPABH/{rl}"
    else:  
        rl = random.randint(242, 255)
        url = f"https://t.me/iuABH/{rl}"  

    caption = "ابن هاشم (رض) مرات متواضع ،🌚 @K_4x1"

    try:
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)
    except Exception:
        await event.reply("⚠️ لم أتمكن من إرسال الفيديو. تأكد أن الفيديو متاح.")

# تشغيل البوت حتى يتم إيقافه
ABH.run_until_disconnected()
