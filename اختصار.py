from telethon import events
from ABH import ABH
import redis

r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
commands={'رفع مطور ثانوي':'promote_secondary_dev','تنزيل مطور ثانوي':'remove_secondary_dev','المطوريين الثانويين':'list_secondary_devs','ارسل':'send_handler','اوامري':'myhandlers','الاوامر':'myhandlers','تفاعل البوت':'stats_handler','تغيير لقبي':'change_own_rank'}
shorten_session={}

def get_all_commands():
    redis_cmds=r.hgetall("commands")
    merged=commands.copy()
    merged.update(redis_cmds)
    return merged

@ABH.on(events.NewMessage(pattern='^اختصار$'))
async def shorten(event):
    user_id=event.sender_id
    if event.chat_id not in shorten_session:
        shorten_session[event.chat_id]={}
    if user_id not in shorten_session[event.chat_id]:
        shorten_session[event.chat_id][user_id]={'step':1}
        await event.reply('ارسل اسم الامر القديم لاختصاره')

@ABH.on(events.NewMessage())
async def handle_shortening_or_command(event):
    text=event.raw_text.strip()
    user_id=event.sender_id
    chat_id=event.chat_id
    if text=="اختصار":
        return
    if chat_id in shorten_session and user_id in shorten_session[chat_id]:
        step_data=shorten_session[chat_id][user_id]
        step=step_data['step']
        if step==1:
            old_command=text
            all_cmds=get_all_commands()
            if old_command in all_cmds:
                shorten_session[chat_id][user_id]={'step':2,'old_command':old_command}
                await event.reply(f'تم العثور على الامر "{old_command}". الآن ارسل الامر المختصر الجديد.')
            else:
                await event.reply(f'الامر "{old_command}" غير موجود في قائمة الاوامر.')
                shorten_session[chat_id].pop(user_id,None)
        elif step==2:
            new_command=text
            old_command=step_data['old_command']
            if new_command:
                handler=get_all_commands()[old_command]
                r.hset("commands",new_command,handler)
                await event.reply(f'تم اختصار "{old_command}" إلى "{new_command}" بنجاح ✅')
            else:
                await event.reply('يرجى ارسال اسم صحيح للاختصار.')
            shorten_session[chat_id].pop(user_id,None)
        return
    all_cmds=get_all_commands()
    for cmd,handler_name in all_cmds.items():
        if text.startswith(cmd):
            func=globals().get(handler_name)
            if func:
                await func(event)
            else:
                await event.reply(f"⚠️ الهاندلر {handler_name} غير معرف بعد.")
            break
