from ABH import ABH #type: ignore
from datetime import datetime
from telethon import events
from other import botuse
import asyncio, os, json
DATA_FILE = "uinfo.json"
DATA_FILE_WEAK = "uinfoWEAK.json"
RESET_FILE = "last_reset.txt"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def load_json(file):
    if os.path.exists(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[تحذير] فشل تحميل JSON من {file} بسبب: {e}")
            os.rename(file, file + ".broken")
            return {}
    return {}
def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def last_reset_date():
    if os.path.exists(RESET_FILE):
        with open(RESET_FILE, 'r') as f:
            return f.read().strip()
    return ""
def update_reset_date(date_str):
    with open(RESET_FILE, 'w') as f:
        f.write(date_str)
uinfo = load_json(DATA_FILE)
WEAK = load_json(DATA_FILE_WEAK)
@ABH.on(events.NewMessage)
async def msgs(event):
    global uinfo, WEAK
    if event.is_group:
        now = datetime.now()
        weekday = now.weekday()
        current_date = now.strftime("%Y-%m-%d")
        uid = event.sender.first_name if event.sender else "الاسم غير متوفر"
        unm = str(event.sender_id)
        guid = str(event.chat_id)
        if weekday == 4 and current_date != last_reset_date():
            WEAK = {}
            save_json(DATA_FILE_WEAK, WEAK)
            update_reset_date(current_date)
        if unm not in uinfo:
            uinfo[unm] = {}
        if guid not in uinfo[unm]:
            uinfo[unm][guid] = {"msg": 0, "guid": guid, "unm": unm, "fname": uid}
        uinfo[unm][guid]["msg"] += 1
        uinfo[unm][guid]["fname"] = uid
        save_json(DATA_FILE, uinfo)
        if unm not in WEAK:
            WEAK[unm] = {}
        if guid not in WEAK[unm]:
            WEAK[unm][guid] = {"msg": 0, "guid": guid, "unm": unm, "fname": uid}
        WEAK[unm][guid]["msg"] += 1
        WEAK[unm][guid]["fname"] = uid
        save_json(DATA_FILE_WEAK, WEAK)
def clean_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        try:
            data = json.loads("".join(lines))
            return data
        except json.JSONDecodeError as e:
            error_line = e.lineno - 1
            print(f"🛠 حذف السطر المعطوب رقم {e.lineno}: {lines[error_line].strip()}")
            lines.pop(error_line)
    print(" لم نتمكن من إصلاح الملف.")
    return {}
fixed_data = clean_json_file("uinfo.json")
if fixed_data:
    with open("uinfo.json", "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
@ABH.on(events.NewMessage)
async def msgs(event):
    global uinfo
    if event.is_group:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        uid = event.sender.first_name if event.sender else "الاسم غير متوفر"
        unm = str(event.sender_id)
        guid = str(event.chat_id)
        if current_time == "00:00":
            for user_id in uinfo:
                for group_id in uinfo[user_id]:
                    uinfo[user_id][group_id]["msg"] = 0
            save_data(uinfo)
        if unm not in uinfo:
            uinfo[unm] = {}
        if guid not in uinfo[unm]:
            uinfo[unm][guid] = {"msg": 0, "guid": guid, "unm": unm, "fname": uid}
        uinfo[unm][guid]["msg"] += 1
        uinfo[unm][guid]["fname"] = uid
        save_data(uinfo)
@ABH.on(events.NewMessage(pattern="^توب اليومي|المتفاعلين$"))
async def اليومي(event):
    type = "المتفاعلين"
    await botuse(type)
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
@ABH.on(events.NewMessage(pattern="^توب الاسبوعي|تفاعل$"))
async def الاسبوعي(event):
    type = "تفاعل"
    await botuse(type)
    guid = str(event.chat_id)
    sorted_users = sorted(
        WEAK.items(),
        key=lambda x: x[1].get(guid, {}).get('msg', 0),
        reverse=True
    )[:10]
    top_users = []
    for idx, (user, data) in enumerate(sorted_users, 1):
        if guid in data:
            fname = data[guid].get('fname', 'مجهول')
            msg_count = data[guid]["msg"]
            top_users.append(f"{idx}. [{fname}](tg://user?id={user}) - {msg_count} رسالة")
    if top_users:
        x = await event.reply("\n".join(top_users))
        await asyncio.sleep(60)
        await x.delete()
    else:
        await event.reply("لا توجد بيانات لعرضها.")
@ABH.on(events.NewMessage(pattern='رسائلي'))
async def show_my_res(event):
    type = "رسائلي"
    await botuse(type)
    await asyncio.sleep(2)
    uid1 = event.sender.first_name
    unm1 = str(event.sender_id)
    guid1 = str(event.chat_id)

    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسلت {msg_count} رسالة في هذه المجموعة.")
@ABH.on(events.NewMessage(pattern=r'^(رسائله|رسائلة|رسائل)$'))
async def his_res(event):
    type = "رسائله"
    await botuse(type)
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
    type = "اوامر التوب"
    await botuse(type)
    await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `المتفاعلين` | `توب اليومي` ل اضهار توب 15 تفاعل \n ارسل `تفاعل` | `توب الاسبوعي` ل اظهار تفاعل المجموعه في اسبوع \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')
