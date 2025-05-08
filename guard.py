from ABH import ABH, events
from Resources import group
from telethon.tl.types import MessageEntityUrl
import asyncio
@ABH.on(events.MessageEdited)
async def edited(event):
    msg = event.message
    chat = event.chat_id
    if chat != group:
        return
    if not msg.edit_date:
        return
    if msg.entities:
        if any(isinstance(entity, MessageEntityUrl) for entity in msg.entities):
            return
    has_media = bool(msg.media)
    has_document = bool(msg.document)
    has_url = any(isinstance(entity, MessageEntityUrl) for entity in (msg.entities or []))
    perms = await ABH.get_permissions(event.chat_id, event.sender_id)
    uid = event.sender_id
    if (has_media or has_document or has_url) and not perms.is_admin:
        await asyncio.sleep(60)
        await event.delete()
