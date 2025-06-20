@ABH.on(events.NewMessage)
async def savegandp(event):
    if event.is_group:
        chat_id = str(event.chat_id)
        r.sadd("all_chats", chat_id)
        r.hset(f"chat:{chat_id}:info", mapping={
            "name": event.chat.title.encode(),
            "type": "group"
        })
    elif event.is_private:
        chat_id = str(event.sender_id)
        r.sadd("all_chats", chat_id)
        r.hset(f"chat:{chat_id}:info", mapping={
            "name": event.sender.first_name.encode() if event.sender.first_name else b'Unknown',
            "type": "private"
        })
    else:
        return
@ABH.on(events.NewMessage(pattern=r'^عرض المسجلين$', from_users=[wfffp]))
async def list_chats(event):
    chat_ids = r.smembers("all_chats")
    if not chat_ids:
        return await event.reply("❗ لا توجد سجلات حالياً.")
    result = "📋 قائمة المسجلين:\n"
    for cid in chat_ids:
        cid = cid.decode() if isinstance(cid, bytes) else cid
        info = r.hgetall(f"chat:{cid}:info")
        name = info.get(b'name', b'Unknown').decode()
        typ = info.get(b'type', b'Unknown').decode()
        result += f"• {name} - `{cid}`\nالنوع: `{typ}`\n\n"
    await event.reply(result)
