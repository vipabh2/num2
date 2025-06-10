from telethon.tl.types import (
    MessageMediaDocument,
    DocumentAttributeAudio)
from other import is_assistant
from telethon import events
from ABH import ABH
import os, json
FILE_PATH = "media_messages.json"
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        media_messages = json.load(f)
else:
    media_messages = {}
def save_media_messages():
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(media_messages, f, ensure_ascii=False, indent=2)
@ABH.on(events.NewMessage())
async def store_media_messages(event):
    chat_id = str(event.chat_id)
    msg = event.message
    if msg.media:
        if isinstance(msg.media, MessageMediaDocument):
            if any(isinstance(attr, DocumentAttributeAudio) for attr in msg.media.document.attributes):
                return
        if chat_id not in media_messages:
            media_messages[chat_id] = []
        if msg.id not in media_messages[chat_id]:
            media_messages[chat_id].append(msg.id)
            save_media_messages()
@ABH.on(events.NewMessage(pattern='^امسح|تنظيف$'))
async def delete_stored_media(event):
    if not is_assistant(event.chat_id, event.sender_id):
        await event.reply('شني خالي كبينه انت مو معاون')
        return
    chat_id = str(event.chat_id)
    deleted_count = 0
    if chat_id in media_messages and media_messages[chat_id]:
        for msg_id in media_messages[chat_id]:
            await ABH.delete_messages(int(chat_id), msg_id)
            deleted_count += 1
        media_messages[chat_id] = []
        save_media_messages()
        await event.reply(f'تم حذف {deleted_count} ب نجاح 🗑️🗑️')
@ABH.on(events.NewMessage(pattern='^عدد|كشف ميديا|كشف الميديا$'))
async def count_media_messages(event):
    chat_id = str(event.chat_id)
    if chat_id in media_messages and media_messages[chat_id]:
        count = len(media_messages[chat_id])
        await event.reply(f'عدد الرسائل الموجهه للحذف {count} 👍🏾')        
    else:
        await event.reply("المجموعة ما بيها ميديا مخزنه للحذف")
@ABH.on(events.NewMessage(pattern='^ثبتها| تخطي المسح|الغاء مسح$'))
async def undel(event):
    if not is_assistant(event.chat_id, event.sender_id):
        await event.reply('شني خالي كبينه انت مو معاون')
        return
    r = await event.get_reply_message()
    if not r:
        await event.reply('يجب الرد على رسالة وسائط.')
        return
    if not r.media:
        await event.reply('يا لوتي لازم ترد على رساله بيها ميديا')
        return
    chat_id = str(event.chat_id)
    msg_id = r.id
    if chat_id in media_messages and msg_id in media_messages[chat_id]:
        media_messages[chat_id].remove(msg_id)
        save_media_messages()
        await event.reply("👌 تم استثناء هذه الرسالة من الحذف.")
    else:
        await event.reply("الرسالة هاي بالاصل ما مسجلة ```ما تنحذف يمي```")
