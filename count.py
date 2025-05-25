from ABH import ABH #type: ignore
from datetime import datetime
from telethon import events
import asyncio, os, json
DATA_FILE_WEAK = "uinfoWEAK.json"
DATA_FILE = "uinfo.json"
def load_dataWEAK():
    if os.path.exists(DATA_FILE_WEAK):
        with open(DATA_FILE_WEAK, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
def save_dataWEAK(data):
    with open(DATA_FILE_WEAK, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
uinfo = load_data()
WEAK = load_dataWEAK()
@ABH.on(events.NewMessage)
async def msgs(event):
    global uinfo, WEAK
    if event.is_group:
        now = datetime.now()
        weekday = now.weekday()
        current_time = now.strftime("%H:%M")
        uid = event.sender.first_name if event.sender else "الاسم غير متوفر"
        unm = str(event.sender_id)
        guid = str(event.chat_id)
        if weekday == 4 and current_time == "00:00":
            WEAK = {}
            save_dataWEAK(WEAK)
        if unm not in uinfo:
            uinfo[unm] = {}
        if guid not in uinfo[unm]:
            uinfo[unm][guid] = {"msg": 0, "guid": guid, "unm": unm, "fname": uid}
        uinfo[unm][guid]["msg"] += 1
        uinfo[unm][guid]["fname"] = uid
        save_data(uinfo)
        if unm not in WEAK:
            WEAK[unm] = {}
        if guid not in WEAK[unm]:
            WEAK[unm][guid] = {"msg": 0, "guid": guid, "unm": unm, "fname": uid}
        WEAK[unm][guid]["msg"] += 1
        WEAK[unm][guid]["fname"] = uid
        save_dataWEAK(WEAK)
@ABH.on(events.NewMessage(pattern="توب اليومي|المتفاعلين"))
async def show_res(event):
    await asyncio.sleep(1)
    guid = str(event.chat_id)
    sorted_users = sorted(
        uinfo.items(), 
        key=lambda x: x[1].get(guid, {}).get('msg', 0), 
        reverse=True
    )[:10]

    top_users = []
    for user, data in sorted_users:
        if guid in data:
            first_name = data[guid].get('fname', 'مجهول')
            user_id = user
            msg_count = data[guid]["msg"]
            top_users.append(f"المستخدم [{first_name}](tg://user?id={user_id}) رسائله -> {msg_count}")
    if top_users:
        x = await event.reply("\n".join(top_users))
        await asyncio.sleep(60)
        await x.delete()
    else:
        await event.reply("لا توجد بيانات لعرضها.")
@ABH.on(events.NewMessage(pattern="توب الاسبوعي|تفاعل"))
async def show_res(event):
    await asyncio.sleep(1)
    guid = str(event.chat_id)
    sorted_users = sorted(
        WEAK.items(), 
        key=lambda x: x[1].get(guid, {}).get('msg', 0), 
        reverse=True
    )[:10]

    top_users = []
    for user, data in sorted_users:
        if guid in data:
            first_name = data[guid].get('fname', 'مجهول')
            user_id = user
            msg_count = data[guid]["msg"]
            top_users.append(f"المستخدم [{first_name}](tg://user?id={user_id}) رسائله -> {msg_count}")
    if top_users:
        x = await event.reply("\n".join(top_users))
        await asyncio.sleep(60)
        await x.delete()
    else:
        await event.reply("لا توجد بيانات لعرضها.")
@ABH.on(events.NewMessage(pattern='رسائلي'))
async def show_my_res(event):
    await asyncio.sleep(2)
    uid1 = event.sender.first_name
    unm1 = str(event.sender_id)
    guid1 = str(event.chat_id)

    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسلت {msg_count} رسالة في هذه المجموعة.")
@ABH.on(events.NewMessage(pattern=r'^(رسائله|رسائلة|رسائل)$'))
async def his_res(event):
    r = await event.get_reply_message()  
    await asyncio.sleep(1)
    if not r:
        return
    uid1 = r.sender.first_name
    unm1 = str(r.sender_id)
    guid1 = str(event.chat_id)
    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسل {msg_count} رسالة في هذه المجموعة.")
@ABH.on(events.NewMessage(pattern='^اوامر التوب$'))
async def title(event):
    await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `المتفاعلين` | `توب اليومي` ل اضهار توب 15 تفاعل \n ارسل `تفاعل` | `توب الاسبوعي` ل اظهار تفاعل المجموعه في اسبوع \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')
