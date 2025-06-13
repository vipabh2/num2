from Program import chs
from Resources import group
from ABH import ABH, events
from telethon import Button
from other import botuse
import random
abh = [
    "ها",
    "تفظل",
    "كول",
    "اسمعك",
    "شرايد",
    "خلصني"
]
@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def anymous(event):
    if event.is_reply or event.is_group:
        return
    type = "مخفي"
    await botuse(type)
    vipabh = random.choice(abh)
    await chs(event, vipabh)
@ABH.on(events.NewMessage(pattern=r'^ابن هاشم$'))
async def ABN_HASHEM(event):
    type = "ابن هاشم"
    await botuse(type)
    caption = "أبن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
    button = [Button.url(text="click", url="https://t.me/wfffp")]
    pic = 'links/photo_2025-02-08_00-25-24.jpg'
    await event.client.send_file(event.chat_id, pic, caption=caption, reply_to=event.message.id, buttons=button)
@ABH.on(events.NewMessage)
async def replys(event):
    if not event.is_group:
        return
    text = event.text
    x = "ادونيس"
    a = 'ابو ذيبه'
    c = event.chat_id
    if x in text and int(c) == int(group):
        await event.reply("@rizrz")
        type = "ادونيس"
        await botuse(type)
    elif a in text and int(c) == int(group):
        await event.reply("@AlconALI")
        type = "ابو ذيبه"
        await botuse(type)
@ABH.on(events.NewMessage(pattern='امير'))
async def reply_amer(event):
    if event.chat_id == group or not event.is_group:
        type = "امير"
        await botuse(type)
        ur = ["https://files.catbox.moe/k44qq6.mp4",
               'https://t.me/KQK4Q/23',
               'https://t.me/KQK4Q/22'
               ]
        url = random.choice(ur)
        caption = "@xcxx1x" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='مقتد'))
async def reply_moqtada(event):
    if not event.is_group:
        return
    if event.chat_id == group:
        type = "مقتدى"
        await botuse(type)
        await event.reply('@hiz8s')
    else: 
        return
auto = [
        "ع س",
        "عليكم السلام",
        "عليكم السلام والرحمة والاكرام",
        "عليكم سلام الله"
        ]
@ABH.on(events.NewMessage(pattern=r'^(سلام عليكم|السلام عليكم)$'))
async def reply_hi(event):
    if not event.is_group:
        return
    type = "السلام عليكم"
    await botuse(type)
    abh = random.choice(auto)
    await event.reply(abh)
@ABH.on(events.NewMessage(pattern='النازية|الشعار'))
async def nazi(event):
    type = "النازية"
    await botuse(type)
    n1 = """🟥🟥🟥🟥🟥🟥🟥🟥🟥
🟥⬜⬜⬜⬜⬜⬜⬜🟥
🟥⬜⬛⬜⬛⬛⬛⬜🟥
🟥⬜️⬛️⬜️⬛️⬜️⬜️⬜️🟥
🟥⬜️⬛️⬛️⬛️⬛️⬛️⬜️🟥
🟥⬜️⬜️⬜️⬛️⬜️⬛️⬜️🟥
🟥⬜️⬛️⬛️⬛️⬜️⬛️⬜️🟥
🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️🟥
🟥🟥🟥🟥🟥🟥🟥🟥🟥
"""
    n2 = """⠙⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢹⠿⣿⣿⣿⣿⣿
⣷⣶⡀⠿⠿⣿⣿⣿⣿⣿⣿⡇⠐⠂⢒⡢⠀⣿⣿⣿
⣿⣿⣿⣆⠀⠈⢻⣿⣿⣿⣿⣿⡆⢈⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⣄⠀⠙⠻⢻⢿⣿⠷⢠⢽⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠁⠀⢘⣱⣍⠿⣾⢿⣿⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⢉⢷⣌⠳⣿⣽⣛⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠋⠽⠶⡌⣿⣻⣀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⡀⠀⠀⠀⠐⠇⢿⣿⣿
⠿⠿⠿⠿⠿⠿⠿⠿⠏⠁⠀⠈⠀⠅⠶⠲⠶⠆⠔⠿"""
    n3 = """⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠛⠉⣩⣍⠉⠛⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠋⠀⠀⣠⣾⣿⠟⠁⠀⠀⠀⠙⣿⣿⣿⣿
⣿⣿⣿⠁⠀⠀⢾⣿⣟⠁⠀⣠⣾⣷⣄⠀⠘⣿⣿⣿
⣿⣿⡇⣠⣦⡀⠀⠙⢿⣷⣾⡿⠋⠻⣿⣷⣄⢸⣿⣿
⣿⣿⡇⠙⢿⣿⣦⣠⣾⡿⢿⣷⣄⠀⠈⠻⠋⢸⣿⣿
⣿⣿⣿⡀⠀⠙⢿⡿⠋⠀⢀⣽⣿⡷⠀⠀⢠⣿⣿⣿
⣿⣿⣿⣿⣄⠀⠀⠀⢀⣴⣿⡿⠋⠀⠀⣠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⣤⣀⣙⣋⣀⣤⣴⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
    abh = random.choice([n1, n2, n3])
    await chs(event, abh)
