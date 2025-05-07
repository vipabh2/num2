from config import *
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    uid = event.sender_id
    r = await event.get_reply_message()
    if uid == 1910015590:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = r.sender_id
        add_points(user_id, gid, points, amount=p)
        await event.reply(f"تم اضافة {p} دينار ل {r.sender.first_name}")
print("top is running")
