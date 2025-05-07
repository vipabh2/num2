from code import *
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    uid = event.sender_id
    r = await event.get_reply_message()
    if uid == wfffp:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = r.sender_id
        add_points(user_id, gid, points, amount=p)
