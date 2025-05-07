from code import ABH, events, wfffp, add_points, points
@ABH.on(events.NewMessage(pattern=r'^اضف فلوس (\d+)$'))
async def add_money(event):
    uid = event.sender_id
    if uid == wfffp:
        p = int(event.pattern_match.group(1))
        gid = event.chat_id
        user_id = event.sender_id
        add_points(user_id, gid, points, amount=p)
