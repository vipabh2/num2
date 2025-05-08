from ABH import ABH, events
import os, json
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
