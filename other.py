from database import store_whisper, get_whisper #type: ignore
from playwright.async_api import async_playwright 
import asyncio, os, json, random, uuid, operator
from ABH import ABH, events, Button
@ABH.on(events.NewMessage(pattern='عاشوراء'))
async def ashourau(event):
    pic = "links/abh.jpg"
    await ABH.send_file(event.chat_id, pic, caption="تقبل الله صالح الأعمال", reply_to=event.message.id)
operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}
@ABH.on(events.NewMessage(pattern=r'احسب (\d+)\s*([\+\-\*/÷])\s*(\d+)'))
async def calc(event):
    try:
        match = event.pattern_match 
        a = int(match.group(1))
        mark = match.group(2)
        b = int(match.group(3))
        if mark in operations:
            result = operations[mark](a, b)
            await event.respond(f"النتيجة `{result}`", reply_to=event.message.id)
        else:
            await event.respond("عملية غير مدعومة!", reply_to=event.message.id)
    except ZeroDivisionError:
        await event.respond("خطأ: لا يمكن القسمة على صفر!", reply_to=event.message.id)

@ABH.on(events.NewMessage(pattern='ميم|ميمز'))
async def meme(event):
    global c
    rl = random.randint(2, 273)
    url = f"https://t.me/IUABH/{rl}"
    cap = random.choice(c)
    await ABH.send_file(event.chat_id, url, caption=f"{cap}", reply_to=event.id)
@ABH.on(events.InlineQuery)
async def Whisper(event):
    builder = event.builder
    query = event.text
    sender = event.sender_id
    if query.strip():
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            recipient = parts[-1]
            try:
                if recipient.isdigit():
                    reciver_id = int(recipient)
                    username = f'ID:{reciver_id}'
                else:
                    if not recipient.startswith('@'):
                        recipient = f'@{recipient}'
                    reciver = await ABH.get_entity(recipient)
                    reciver_id = reciver.id
                    username = recipient
                whisper_id = str(uuid.uuid4())
                store_whisper(whisper_id, sender, reciver_id, username, message)
                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي 😌 ({username})",
                    buttons=[
                        Button.inline(
                            text='🫵🏾 اضغط لعرض الهمسة',
                            data=f'send:{whisper_id}'
                        )
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                    # text=f' خطأ: {str(e)}'
                )
        else:
            return
        await event.answer([result])
@ABH.on(events.CallbackQuery)
async def callback_Whisper(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        whisper_id = data.split(':')[1]
        whisper = get_whisper(whisper_id)
        if whisper:
            if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                await event.answer(f"{whisper.message}", alert=True)
            else:
                await event.answer("عزيزي الحشري، هذه الهمسة ليست موجهة إليك!", alert=True)
BANNED_SITES = [
    "porn", "xvideos", "xnxx", "redtube", "xhamster",
    "brazzers", "youjizz", "spankbang", "erotic", "sex"
]
DEVICES = {
    "pc": {"width": 1920, "height": 1080, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    "android": "Galaxy S5"
}
async def take_screenshot(url, device="pc"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        if device in DEVICES:
            if isinstance(DEVICES[device], str):
                device_preset = p.devices[DEVICES[device]]
                context = await browser.new_context(**device_preset)
            else:
                context = await browser.new_context(
                    user_agent=DEVICES[device]["user_agent"],
                    viewport={"width": DEVICES[device]["width"], "height": DEVICES[device]["height"]}
                )
            page = await context.new_page()
        else:
            page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)
            screenshot_path = f"screenshot_{device}.png"
            await page.screenshot(path=screenshot_path)
        except Exception as e:
            screenshot_path = None
        finally:
            await browser.close()
    return screenshot_path
@ABH.on(events.NewMessage(pattern=r'كشف رابط|سكرين (.+)'))
async def screen_shot(event):
    url = event.pattern_match.group(1)
    if any(banned in url.lower() for banned in BANNED_SITES):
        await event.reply("🚫 هذا الموقع محظور!\nجرب تتواصل مع المطور @k_4x1")
        return
    devices = ['pc', 'android']
    screenshot_paths = []
    for device in devices:
        screenshot_path = await take_screenshot(url, device)
        if screenshot_path:
            screenshot_paths.append(screenshot_path)
    if screenshot_paths:
        await event.reply(f"✅ تم التقاط لقطات الشاشة للأجهزة: **PC، Android**", file=screenshot_paths)
        await asyncio.sleep(60)
        await event.delete()
    else:
        await event.reply("❌ فشل التقاط لقطة الشاشة، تأكد من صحة الرابط أو جرب مجددًا.")
FILE = "dialogs.json"
K_4X1 = 1910015590
def load_alert():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return set(json.load(f))
    return set()
def save_alerts():
    with open(FILE, "w") as f:
        json.dump(list(alert_ids), f)
alert_ids = load_alert()
async def alert(message):
    try:
        await ABH.send_message(K_4X1, message)
    except Exception as e:
        return
@ABH.on(events.NewMessage)
async def add_to(event):
    global alert_ids
    chat = await event.get_chat()
    if chat.id not in alert_ids:
        try:
            alert_ids.add(chat.id)
            save_alerts()
            chat_name = chat.title if hasattr(chat, 'title') else chat.first_name
            return
        except Exception as e:
            await alert(f"فشل إضافة المحادثة: {chat_name} \n {chat.id} - {e} ")
@ABH.on(events.NewMessage(pattern="/alert"))
async def send_alert(event):
    if event.sender_id != K_4X1:
        return
    message_text = None
    if event.reply_to_msg_id:
        replied_msg = await event.get_reply_message()
        message_text = replied_msg.text
    else:
        command_parts = event.raw_text.split(maxsplit=1)
        if len(command_parts) > 1:
            message_text = command_parts[1]
    if not message_text:
        await event.reply("يرجى الرد على رسالة أو كتابة نص بعد `/alert`.")
        return
    await event.reply(f"🚀 جاري إرسال التنبيه إلى {len(alert_ids)} محادثة...")
    for dialog_id in alert_ids:
        try:
            await ABH.send_message(dialog_id, f"**{message_text}**")
            await alert(f"✅ تم الإرسال إلى: {dialog_id}")
        except Exception as e:
            await alert(f"❌ فشل الإرسال إلى {dialog_id}: {e}")
    await event.reply("✅ تم إرسال التنبيه لجميع المحادثات!")
