from telethon import events, Button
from other import wfffp
import os, json, redis
from ABH import ABH
CHANNEL_KEY = 'ANYMOUSupdate'
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
async def chs(event, c):
    buttons = Button.url('🫆', url=f'https://t.me/{CHANNEL_KEY}')
    await ABH.send_message(event.chat_id, c, reply_to=event.id, buttons=buttons)
@ABH.on(events.NewMessage(pattern=r'^تعيين القناة (.+)', from_users=[wfffp]))
async def add_channel(event):
    global CHANNEL_KEY
    ch = event.pattern_match.group(1)
    x = r.exists(CHANNEL_KEY)
    if x:
        r.delete(CHANNEL_KEY)
    r.set(CHANNEL_KEY, ch)
    await event.reply(f" تم حفظ القناة {ch}")
    CHANNEL_KEY = ch
@ABH.on(events.NewMessage(pattern=r'^عرض القناة$', from_users=[wfffp]))
async def show_channel(event):
    ch = r.get(CHANNEL_KEY)
    if ch:
        await event.reply(f"📡 القناة المحفوظة: {ch}")
    else:
        await event.reply("⚠️ لا توجد قناة محفوظة.")
@ABH.on(events.NewMessage(pattern=r'^تفاعل البوت$', from_users=[wfffp]))
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
@ABH.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    if event.is_private:
        buttons = [
            Button.url(
            "لرفعي مشرف",
                url="https://t.me/vipabh_bot?startgroup=Commands&admin=ban_users+delete_messages+restrict_members+invite_users+pin_messages+change_info+add_admins+promote_members+manage_call+manage_chat+manage_video_chats+post_stories+edit_stories+delete_stories"
    ),
            Button.url(
                "تحديثات البوت",
                url=f"https://t.me/{CHANNEL_KEY}"
    )
]
        await ABH.send_message(event.chat_id, "اهلا حياك الله \n مخفي لحماية المجموعة واوامر خدميه واللعاب جديدة \n علمود اشتغل بسلاسه لازم ترفعني مشرف عبر الزر الموجود 👇", buttons=buttons, reply_to=event.id)
@ABH.on(events.NewMessage)
async def savegandp(event):
    chat_id = event.chat_id
    chat_type = (
        "private" if event.is_private else
        "group" if event.is_group else
        "channel" if event.is_channel else "unknown"
    )
    if chat_type == "unknown":
        return
    redis_key = f"chat:{chat_id}:info"
    if not r.exists(redis_key):
        try:
            chat = await event.get_chat()
            if event.is_private:
                first = chat.first_name or ""
                last = chat.last_name or ""
                name = (first + " " + last).strip() or (chat.username or "مستخدم غير معرف")
            else:
                name = chat.title or chat.username or "دردشة غير معرفة"
        except:
            name = "غير معروف"
        r.hset(redis_key, mapping={
            "name": name,
            "type": chat_type
        })
        r.sadd("all_chats", chat_id)
        msg = f"""🔔 تم تسجيل جديد:
• الاسم: {name}
• ID: {chat_id}
• النوع: {chat_type}"""
        await ABH.send_message(wfffp, msg)
@ABH.on(events.NewMessage(pattern=r'^عرض المسجلين$', from_users=[wfffp]))
async def list_chats(event):
    chat_ids = r.smembers("all_chats")
    if not chat_ids:
        return await event.reply("❗ لا توجد سجلات حالياً.")
    result = "📋 قائمة المسجلين:\n"
    for cid in chat_ids:
        cid = cid.decode() if isinstance(cid, bytes) else cid
        info = r.hgetall(f"chat:{cid}:info")
        name = info.get(b'name', b'غير معروف').decode()
        typ = info.get(b'type', b'غير معروف').decode()
        result += f"• {name} - {cid}\nالنوع: {typ}\n\n"
    await event.reply(result)
