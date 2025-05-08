from ABH import ABH, events
abh = [
    "ها",
    "تفظل",
    "كول",
    "اسمعك",
    "شرايد",
    "خلصني",
    "https://t.me/VIPABH/1214",
    "https://t.me/VIPABH/1215"
]
@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def anymous(event):
    if event.is_reply:
        return
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)
@ABH.on(events.NewMessage)
async def replys(event):
    text = event.text
    x = "ادونيس"
    c = event.chat_id
    if x in text and int(c) == int(group):
        await event.reply("@rizrz")
    abh = "ابن هاشم"
    if abh in text:
        rl = random.randint(1222, 1241)
        url = f"https://t.me/VIPABH/{rl}"
        caption = "أبن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
        button = [Button.url(text="click", url="https://t.me/K_4x1")]
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id, buttons=button)
@ABH.on(events.NewMessage(pattern='زهراء'))
async def reply_zahraa(event):
    if event.chat_id == group:
        url = "https://t.me/VIPABH/1220"  
        caption = "@klix_78 ( لَقَدْ كَفَرَ الّذِينَ قَالُوا إنَّ الله هُو المَسِيحُ ابْنُ مَرْيَم)." 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='امير'))
async def reply_amer(event):
    if event.chat_id == group:
        ur = ["https://files.catbox.moe/k44qq6.mp4",
               'https://t.me/KQK4Q/23',
               'https://t.me/KQK4Q/22'
               ]
        url = random.choice(ur)
        caption = "@xcxx1x" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='محمد موسى'))
async def reply_mohamed(event):
    if event.chat_id == group:
        await event.reply('@E_0_0_0 ')
    else: 
        return
@ABH.on(events.NewMessage(pattern='هاكس'))
async def reply_mohamed(event):
    if event.chat_id == group:
        await event.reply('@c7cce')
    else: 
        return
@ABH.on(events.NewMessage(pattern='مقتد'))
async def reply_moqtada(event):
    if event.chat_id == group:
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
        abh = random.choice(auto)
        await event.reply(abh)
@ABH.on(events.NewMessage(pattern='النازية|الشعار'))
async def nazi(event):
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
    await event.reply(abh)
