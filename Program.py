from telethon import events, Button
from other import wfffp
import os, json, redis
from ABH import ABH
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
