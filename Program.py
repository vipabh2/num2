from telethon import events
from other import botuse, wfffp
import os, json, redis
from ABH import ABH
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
CHANNEL_KEY = 'saved_channel'
@ABH.on(events.NewMessage(pattern=r'^تعيين القناة (.+)', from_users=[wfffp]))
async def add_channel(event):
    ch = event.pattern_match.group(1)
    r.set(CHANNEL_KEY, ch)
    await event.reply(f" تم حفظ القناة {ch}")
@ABH.on(events.NewMessage(pattern=r'^عرض القناة$'), from_users=[wfffp])
async def show_channel(event):
    ch = r.get(CHANNEL_KEY)
    if ch:
        await event.reply(f"📡 القناة المحفوظة: {ch}")
    else:
        await event.reply("⚠️ لا توجد قناة محفوظة.")
@ABH.on(events.NewMessage(pattern=r'^تفاعل البوت$'), from_users=[wfffp])
async def stats_handler(event):
    if event.sender_id != wfffp:
        return
    try:
        with open('use.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await event.reply("لا توجد بيانات محفوظة بعد.")
        return
    if not data:
        await event.reply("📊 لا توجد أي استخدامات مسجلة بعد.")
        return
    msg = "📈 إحصائيات الاستخدام:\n\n"
    for key, value in sorted(data.items(), key=lambda item: item[1], reverse=True):
        msg += f"• {key} : {value}\n"
    x = event.is_private
    if x:
        await event.reply(msg)
    else:
        await ABH.send_message(wfffp, msg)
        await event.reply('تم الارسال في الخاص')
DATA_FILE = "users_by_type.json"
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"private": {}, "group": {}, "channel": {}}
def save_users(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
@ABH.on(events.NewMessage)
async def log_user_by_type(event):
    user_id = event.sender_id
    name = event.first_name or "بدون اسم"
    username = event.username or "بدون معرف"
    link = f"tg://user?id={event.id}"
    if event.is_private:
        chat_type = "private"
    elif event.is_group:
        chat_type = "group"
    elif event.is_channel:
        chat_type = "channel"
    else:
        return
    data = load_users()
    if user_id not in data[chat_type]:
        data[chat_type][user_id] = {
            "name": name,
            "username": username,
            "link": link
        }
        save_users(data)
@ABH.on(events.NewMessage(pattern=r'^احصائيات$', from_users=1910015590))
async def send_statistics(event):
    data = load_users()
    type = "احصائيات"
    await botuse(type)
    private_count = len(data["private"])
    group_count = len(data["group"])
    channel_count = len(data["channel"])
    total = private_count + group_count + channel_count
    msg = (
        f"**📊 إحصائيات مستخدمي البوت:**\n"
        f"• المستخدمين الخاصين: `{private_count}`\n"
        f"• المجموعات: `{group_count}`\n"
        f"• القنوات: `{channel_count}`\n"
        f"• الإجمالي الكلي: `{total}`\n"
        f"------------------------------\n"
        f"لرؤية التفاصيل، استخدم الأمر:\n`تفاصيل`"
    )
    await event.reply(msg)
@ABH.on(events.NewMessage(pattern=r'^تفاصيل$', from_users=1910015590))
async def send_user_details(event):
    type = "تفاصيل"
    await botuse(type)
    data = load_users()
    msg_parts = []
    for chat_type, users in data.items():
        msg_parts.append(f"\n**{chat_type.upper()}** - ({len(users)}):")
        for user_id, info in users.items():
            name = info["name"]
            username = f"@{info['username']}" if info["username"] != "بدون معرف" else "لا يوجد"
            link = info["link"]
            msg_parts.append(f"- [{name}]({link}) | {username}")
    full_msg = "\n".join(msg_parts)    
    if len(full_msg) > 4000:
        await event.reply("📤 عدد كبير من المستخدمين، يتم إرسال التفاصيل برسائل متعددة...")
        for i in range(0, len(full_msg), 4000):
            await event.reply(full_msg[i:i+4000], parse_mode="markdown")
    else:
        await event.reply(full_msg, parse_mode="markdown")
