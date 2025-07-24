from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChatAdminRights
from top import points, add_user, save_points
from Program import chs
from telethon import events, Button
from Resources import *
from other import botuse
from ABH import ABH
@ABH.on(events.NewMessage(pattern=r"^تغيير لقبي\s*(.*)$"))
async def change_own_rank(event):
    if not event.is_group:
        return
    new_rank = event.pattern_match.group(1)
    if not new_rank:
        await chs(event, "اكتب اللقب وي الامر ك `تغيير لقبي ` + لقب.")
        return
    await botuse("تغيير لقبي")
    user_id = event.sender_id
    chat = await event.get_chat()
    me = await ABH.get_permissions(chat.id, 'me')
    if not me.is_admin or not me.add_admins:
        await chs(event, " لا أمتلك صلاحية تعديل المشرفين.")
        return
    o = await get_owner(event)
    if user_id == o.id:
        await event.reply('هاي عود انت المالك')
        return
    x = await ABH.get_me()
    result = await ABH(GetParticipantRequest(channel=chat.id, participant=user_id))
    if isinstance(result.participant, ChannelParticipantAdmin):
        if result.participant.promoted_by != x.id:
            user = await ABH.get_entity(result.participant.promoted_by)
            menti = await ment(user)
            await chs(event, f"خلي {menti} يعدل لقبك لدوخني توكل")
            return
    if len(new_rank) > 14:
        await chs(event, "اللقب لازم يكون اقل من 14 حرف.")
        return
    try:
        pp = await ABH(GetParticipantRequest(chat.id, user_id))
        participant = pp.participant
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ في جلب بيانات المستخدم: {e}")
        await event.reply(f"والله مابيه حيل اعذرني يخوي")
        return
    if not isinstance(participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
        await chs(event, "يالفقير لازم تكون مشرف بالاول علمود اغيرلك لقب🙄🙄.")
        return
    admin_right = participant.admin_rights
    try:
        await ABH(EditAdminRequest(
            channel=chat.id,
            user_id=user_id,
            admin_rights=admin_right,
            rank=new_rank
        ))
        await chs(event, f"تم تغيير لقبك الى `{new_rank}`")
    except Exception as e:
        await ABH.send_message(wfffp, f"خطأ عند تعديل اللقب: {e}")
        await chs(event, "والله مابيه حيل اعذرني يخوي")
promot = {}
session = {}
@ABH.on(events.NewMessage(pattern='^ترقية$'))
async def promoteADMIN(event):
    if not event.is_group:
        return
    chat = await event.get_chat()
    user_id = event.sender_id
    me = await ABH.get_permissions(chat.id, 'me')
    if not me.is_admin or not me.add_admins:
        await chs(event, " لا أمتلك صلاحية تعديل المشرفين.")
        return
    type = "ترقية"
    await botuse(type)
    isc = await can_add_admins(chat, user_id)
    o = await get_owner(event)
    uid = event.sender_id
    if uid != o.id or uid != wfffp or not isc:
        await chs(event, 'عذرا الامر لا يخصك')
        return
    r = await event.get_reply_message()
    if not r:
        await chs(event, 'لازم تسوي رد لشخص علمود ارفعه')
        return
    chat_id = event.chat_id
    if chat_id not in promot:
        promot[chat_id] = {}
    if chat_id not in session:
        session[chat_id] = {}
    session[chat_id].update({'pid': user_id, 'top': r.sender_id})
    target_user_id = r.sender_id
    promot[chat_id][target_user_id] = {
        'rights': {
            'change_info': False,
            'delete_messages': False,
            'ban_users': False,
            'invite_users': False,
            'pin_messages': False,
            'add_admins': False,
            'manage_call': False,
        },
        'initiator': event.sender_id,
        'top_msg': r.id
    }

    buttons = [
        [Button.inline('تغيير معلومات', data='change_info'), Button.inline('حذف رسائل', data='delete_messages')],
        [Button.inline('حظر المستخدمين', data='ban_users'), Button.inline('دعوة', data='invite_users')],
        [Button.inline('الاتصال', data='manage_call'), Button.inline('اضافة مشرفين', data='add_admins')],
        [Button.inline('تثبيت رسائل', data='pin_messages')],
        [Button.inline('تم', data='done')]
        ]
    c = 'يتم رفع المستخدم مشرف \n يرجى تحديد الصلاحيات'
    await ABH.send_file(
        entity=event.chat_id,
        file='https://t.me/VIPABH/1219',
        caption=c,
        reply_to=event.id,
        buttons=buttons)
@ABH.on(events.CallbackQuery)
async def promoti(event):
    data = event.data.decode('utf-8')
    if data == 'empty':
        await event.answer('الفارغ مو الزر , انت لا ضغطت', alert=True)
    chat_id = event.chat_id
    if chat_id not in session or not session[chat_id]:
        return
    initiator_id = session[chat_id]['pid']
    target_user_id = session[chat_id]['top']
    if event.sender_id != initiator_id:
        await event.answer('ما تكدر تعدل شيء هنا', alert=True)
        return
    if chat_id not in promot or target_user_id not in promot[chat_id]:
        return
    rights = promot[chat_id][target_user_id]['rights']
    if data == 'done':
        await event.answer(' تم تنفيذ الترقية', alert=False)
        await event.edit('تم رفع المستخدم بنجاح \n لتغيير اللقب ارسل ```تغيير لقبي ``` + لقب معين ')
        admin_rights = ChatAdminRights(
            change_info=rights.get('change_info', False),
            delete_messages=rights.get('delete_messages', False),
            ban_users=rights.get('ban_users', False),
            invite_users=rights.get('invite_users', False),
            pin_messages=rights.get('pin_messages', False),
            add_admins=rights.get('add_admins', False),
            manage_call=rights.get('manage_call', False),
            manage_topics = False,
            anonymous = False,
            # post_stories = True,
            # edit_stories = True,
            # delete_stories =  True
        )
        c = 'مشرف'
        await ABH(EditAdminRequest(event.chat_id, target_user_id, admin_rights, rank=c))
        del session[chat_id]
        del promot[chat_id][target_user_id]
        return
    if data not in rights:
        return
    rights[data] = True
    await event.answer(f' تم تفعيل: {data}', alert=False)
@ABH.on(events.NewMessage(pattern=r'رفع سمب(?:\s+(\d+))?'))
async def promote_handler(event):
    if not event.is_group:
        return
    type = "رفع سمب"
    await botuse(type)
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("يجب الرد على شخص حتى ترفعه.")
        return
    match = event.pattern_match
    amount = int(match.group(1)) if match.group(1) else 1001
    uid = str(event.sender_id)
    target_id = str(message.sender_id)
    giver_name = (await event.get_sender()).first_name or "مجهول"
    if target_id == 1910015590:
        await event.reply(f'جاري رفع {giver_name} سمب')
    receiver_name = message.sender.first_name or "مجهول"
    gid = str(event.chat_id)
    add_user(target_id, gid, receiver_name, points, 0)
    add_user(uid, gid, giver_name, points, 0)
    if points[gid][target_id].get("status") == "مرفوع":
        await event.reply(f"{receiver_name} مرفوع من قبل.")
        return
    if amount < 1000:
        await event.reply("أقل مبلغ مسموح للرفع هو 1000.")
        return
    giver_money = points[uid][gid]['points']
    if giver_money < 1000:
        await event.reply(f" رصيدك {giver_money}، والحد الأدنى للرفع هو 10.")
        return
    if giver_money < amount:
        await event.reply(f" رصيدك لا يكفي. تحاول ترفع بـ {amount} فلوس ورصيدك فقط {giver_money}.")
        return
    points[uid][gid]['points'] = giver_money - amount
    points[gid][target_id]["status"] = "مرفوع"
    points[gid][target_id]["giver"] = uid
    points[gid][target_id]["promote_value"] = amount
    save_points(points)
    await event.reply(f" تم رفع {receiver_name} مقابل {amount} فلوس")
@ABH.on(events.NewMessage(pattern='تنزيل سمب'))
async def demote_handler(event):
    if not event.is_group:
        return
    type = "تنزيل سمب"
    await botuse(type)
    message = await event.get_reply_message()
    if not message or not message.sender:
        await event.reply("متكدر تنزل العدم , سوي رد على شخص")
        return
    gid = str(event.chat_id)
    sender_id = str(event.sender_id)
    target_id = str(message.sender_id)
    target_name = message.sender.first_name or "مجهول"
    add_user(target_id, gid, target_name, points, 0)
    add_user(sender_id, gid, event.sender.first_name, points, 0)
    if points[gid].get(target_id, {}).get("status") != "مرفوع":
        await event.reply("المستخدم هاذ ما مرفوع من قبل😐")
        return
    giver_id = points[gid][target_id].get("giver")
    executor_money = points[sender_id][gid]['points']
    promote_value = points[gid][target_id].get("promote_value", 313)
    amount = int(promote_value * (1.5 if sender_id == giver_id else 2))
    if executor_money < amount:
        await event.reply(f"ما تگدر تنزله لأن رصيدك {executor_money}، والكلفة المطلوبة {amount}")
        return
    points[sender_id][gid]['points'] -= amount
    del points[gid][target_id]
    if not points[gid]:
        del points[gid]
    save_points(points)
    r = await event.get_reply_message()
    await event.reply(f"تم تنزيل {r.sender.first_name}  من السمبية")
@ABH.on(events.NewMessage(pattern='السمبات'))
async def show_handler(event):
    if not event.is_group:
        return
    type = "السمبات"
    await botuse(type)
    chat_id = str(event.chat_id)
    if chat_id not in points or not points[chat_id]:
        await event.reply("ماكو سمبات هنا بالمجموعة")
        return
    response = "قائمة السمبات👇\n"
    removed_users = []
    for uid in list(points[chat_id].keys()):
        data = points[chat_id][uid]
        if data.get("status") == "مرفوع":
            status_icon = "👌"
            response += f"{status_icon} [{data['name']}](tg://user?id={uid}) ⇜ {data.get('promote_value', 0)}\n"
        else:
            removed_users.append(uid)
    for uid in removed_users:
        if points[chat_id].get(uid) and points[chat_id][uid].get("status") != "مرفوع":
            del points[chat_id][uid]
    save_points(points)
    await event.reply(response if response.strip() != "قائمة السمبات👇" else "ماكو وردات مرفوعين بالمجموعة", parse_mode="Markdown")
@ABH.on(events.NewMessage(pattern='اوامر الرفع'))
async def promot_list(event):
    if not event.is_group:
        return
    type = "اوامر الرفع"
    await botuse(type)
    await event.reply('**اوامر الرفع كالاتي** \n `رفع سمب` + عدد فلوس \n لرفع الشخص في قائمة `السمبات` \n `تنزيل سمب` \n حتى ترفع لازم يكون رصيدك 1000 والتنزيل يُضرب المبلغ *1.5 \n * `اوامر الالعاب`\n `رفع معاون` بالرد \n حتى ترفع الشخص معاون \n `تنزيل معاون` بالرد \n حتى تنزل الشخص من المعاونين \n `المعاونين` حتى تشوف قائمة المعاونين بالمجموعة \n `رفع معاون` بالرد على مستخدم \n راح ينرفع المستخدم داخل البوت\n \n `المعاونين` علمود تشوف المرفوعين  \n `ترقية` حتى ترفعه مشرف بالمجموعة')
