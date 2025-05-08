from telethon import events
from collections import defaultdict
from datetime import datetime
from ABH import ABH
import asyncio
uinfo = {}
uinfo = defaultdict(lambda: defaultdict(lambda: {"msg": 0}))
@ABH.on(events.NewMessage)
async def msgs(event):
    global uinfo
    if event.is_group:
        now = datetime.now()
        uid = event.sender.first_name if event.sender else "الاسم غير متوفر"
        unm = event.sender_id
        guid = event.chat_id
        user_data = uinfo[unm][guid]
        user_data.update({"guid": guid, "unm": unm, "fname": uid})
        user_data["msg"] += 1
        timenow = now.strftime("%I:%M %p")
        targetdate = "11:59 PM"
        if timenow == targetdate:
            uinfo = defaultdict(lambda: defaultdict(lambda: {"msg": 0}))
@ABH.on(events.NewMessage(pattern="توب اليومي|المتفاعلين"))
async def show_res(event):
    await asyncio.sleep(2)
    guid = event.chat_id
    sorted_users = sorted(
        uinfo.items(), 
        key=lambda x: x[1].get(guid, {}).get('msg', 0), 
        reverse=True
    )[:10]
    top_users = []
    for user, data in sorted_users:
        if guid in data:
            first_name = data.get(guid, {}).get('fname', 'مجهول')
            user_id = user
            msg_count = data[guid]["msg"]
            top_users.append(f"المستخدم [{first_name}](tg://user?id={user_id}) رسائله -> {msg_count}")
    if top_users:
        x = await event.reply("\n".join(top_users))
        asyncio.sleep(60)
        await x.delete()
    else:
        await event.reply("لا توجد بيانات لعرضها.")
@ABH.on(events.NewMessage(pattern='رسائلي'))
async def show_res(event):
    await asyncio.sleep(2)
    uid1 = event.sender.first_name
    unm1 = event.sender_id
    guid1 = event.chat_id
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
    unm1 = r.sender_id
    guid1 = event.chat_id
    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسل {msg_count} رسالة في هذه المجموعة.")
@ABH.on(events.NewMessage(pattern='الرسائل'))
async def title(event):
    # await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `المتفاعلين` ل اضهار توب 15 تفاعل \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')
