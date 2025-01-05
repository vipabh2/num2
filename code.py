from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsBanned
import os

# جلب بيانات البوت من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء العميل الأساسي
client = TelegramClient('s', api_id, api_hash).start(bot_token=bot_token)

async def get_users_without_write_permission(event):
    group_username = event.chat_id  # الحصول على معرف المجموعة من الحدث

    # جلب المشاركين المحظورين فقط باستخدام العميل الأساسي
    participants = await client(GetParticipantsRequest(
        channel=group_username,
        filter=ChannelParticipantsBanned(q=""),  # استخدم قيمة فارغة بدلاً من None
        offset=0,
        limit=100,  # جلب أول 100 مستخدم محظور
        hash=0
    ))

    # إذا لم يكن هناك مشاركون محظورون
    if not participants.users:
        await event.reply("لا يوجد مستخدمون محظورون في هذه المجموعة.")
        return

    # إرسال النتائج للمستخدم الذي أرسل الأمر
    for banned_user in participants.users:
        # إذا كان للمستخدم اسم مستخدم
        mention = f"[@{banned_user.username}](https://t.me/@{banned_user.username})" if banned_user.username else f"[{banned_user.first_name}](tg://user?id={banned_user.id})"
        
        # تحقق من وجود وقت الحظر الفعلي
        if hasattr(banned_user, 'banned_until') and banned_user.banned_until:
            ban_time = banned_user.banned_until.strftime("%Y-%m-%d %H:%M:%S")  # وقت الحظر الفعلي
        else:
            ban_time = "لا يوجد وقت محدد للحظر"

        await event.reply(f"User: {banned_user.id} - {mention}\nTime Banned: {ban_time}", parse_mode="md")

# تشغيل الكود عبر حدث
from telethon import events

@client.on(events.NewMessage(pattern='/get_banned'))  # تشغيل الكود عند كتابة الأمر /get_banned
async def handle_event(event):
    await get_users_without_write_permission(event)

# إبقاء البوت قيد التشغيل
client.run_until_disconnected()
