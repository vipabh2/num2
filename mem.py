from ABH import ABH, events
from other import botuse
import random
@ABH.on(events.NewMessage(pattern=r'^(مخفي طكة زيج|زيج|مخفي اعفطلة)$'))
async def reply_abh(event):
    type = "زيج"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message and replied_message.sender_id == 1910015590:
        await event.reply("الزيج اللك مو للمطور😡")
        return
    if replied_message:
        abh = random.choice([
            'https://t.me/VIPABH/1171',
            'https://t.me/recoursec/7',
            'https://t.me/recoursec/17',
            'https://t.me/recoursec/8'
        ])
        await event.client.send_file(replied_message.peer_id, abh, reply_to=replied_message.id)
    else:
        await event.reply("عزيزي الفاهي ... \n الامر يعمل بالرد , اذا عدتها وما سويت رد اعفطلك")
@ABH.on(events.NewMessage(pattern=r'^(ميعرف|مايعرف)$'))
async def reply_mem(event):
    type = "ميعرف"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/3", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/3", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(صباح النور|صباح الخير)$'))
async def reply_mem(event):
    type = "صباح الخير"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/4", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/4", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(لا تتمادة|لا تتماده|تتماده)$'))
async def reply_mem(event):
    type = "تتمادة"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/5", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/5", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(هيه حسب|هاي بعد|اي هاي)$'))
async def reply_mem(event):
    type = "اي هاي"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/6", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/6", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(يله شنسوي|ههههه)$'))
async def reply_mem(event):
    type = "ههههه"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/9", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/9", reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r'^(man up|استرجل)$'))
async def reply_mem(event):
    type = "استرجل"
    await botuse(type)
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/recoursec/10", reply_to=replied_message)
    else:
        await event.reply(file="https://t.me/recoursec/10", reply_to=event.message.id)
