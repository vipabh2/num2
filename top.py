import json
from ABH import ABH, events
def load_points(filename="points.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_points(data, filename="points.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
points = load_points()
def add_points(uid, gid, points_dict, amount=0):
    uid, gid = str(uid), str(gid)
    if uid not in points_dict:
        points_dict[uid] = {}
    if gid not in points_dict[uid]:
        points_dict[uid][gid] = {"points": 0}
    points_dict[uid][gid]["points"] += amount
    save_points(points_dict)
def add_user(uid, gid, name, rose, amount):
    uid, gid = str(uid), str(gid)
    if gid not in rose:
        rose[gid] = {}
    if uid not in rose[gid]:
        rose[gid][uid] = {
            "name": name,
            "status": "عادي",
            "giver": None,
            "m": amount,
            "promote_value": 0
        }
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
@ABH.on(events.NewMessage(pattern='ثروتي'))
async def m(event):
    uid = str(event.sender_id)
    gid = str(event.chat_id)
    if uid in points and gid in points[uid]:
        m = points[uid][gid]['points']
    else:
        m = 0
    await event.reply(f'فلوسك ↢ ( {m} )')
@ABH.on(events.NewMessage(pattern='ثروته|الثروه'))
async def m(event):
    r = await event.get_reply_message()
    uid = str(r.sender_id)
    gid = str(event.chat_id)
    if uid in points and gid in points[uid]:
        m = points[uid][gid]['points']
    else:
        m = 0
    await event.reply(f'فلوسه ↢ ( {m} )')
print("top is running")
