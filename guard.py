from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, MessageEntityUrl
from Resources import group, mention, ment, hint, react
from other import is_assistant, botuse, is_owner
from telethon import events, Button
from Program import r as redas, chs
import os, asyncio, re, json, time
from top import points, delpoints
from ABH import ABH
@ABH.on(events.NewMessage(pattern=r"^المقيدين عام$"))
async def list_restricted(event):
    chat_id = event.chat_id
    now = int(time.time())
    if chat_id not in restriction_end_times or not restriction_end_times[chat_id]:
        await event.reply("لا يوجد أي مستخدم مقيد حالياً.")
        return
    msg = "📋 قائمة المقيدين عام:\n\n"
    expired_users = []
    for user_id, end_time in list(restriction_end_times[chat_id].items()):
        try:
            user = await ABH.get_entity(user_id)
            name = f"[{user.first_name}](tg://user?id={user_id})"
            remaining = end_time - now
            if remaining > 0:
                minutes, seconds = divmod(remaining, 60)
                msg += f"● {name} ↔ `{user_id}`\n⏱️ باقي: {minutes} دقيقة و {seconds} ثانية\n\n"
            else:
                expired_users.append(user_id)
        except Exception as e:
            msg += f"مستخدم غير معروف — `{user_id}`\n"
            await hint(e)
    for user_id in expired_users:
        del restriction_end_times[chat_id][user_id]
    if msg.strip() == "📋 قائمة المقيدين عام:":
        msg = "✅ لا يوجد حالياً أي مستخدم مقيد."
    await event.reply(msg, link_preview=False)
async def notAssistantres(event):
    if not event.is_group:
        return
    lock_key = f"lock:{event.chat_id}:تقييد"
    if redas.get(lock_key) != "True":
        await chs(event, 'التقييد غير مفعل في هذه المجموعه🙄')
        return
    chat_id = event.chat_id
    user_id = event.sender_id
    sender = await event.get_sender()
    chat = await event.get_chat()
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")    
    rs = await r.get_sender()
    target_name = await ment(rs)
    user_points = points.get(str(user_id), {}).get(str(chat_id), {}).get("points", 0)
    if user_points < 1000000:
        return await event.reply("عزيزي الفقير , لازم ثروتك اكثر من مليون دينار.")
    try:
        participant = await ABH(GetParticipantRequest(channel=chat_id, participant=rs.id))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return await event.reply(f"لا يمكنك تقييد {target_name} لأنه مشرف.")
    except Exception as e:
        return await hint(e)
    user_to_restrict = await r.get_sender()
    user_id = user_to_restrict.id
    now = int(time.time())
    restriction_duration = 30
    rights = ChatBannedRights(
        until_date=now + restriction_duration,
        send_messages=True
    )      
    try:
        await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
    except Exception as e:
        await event.reply("ياريت اقيده بس ماكدر 🥲")
        await hint(e)
    await botuse("تقييد ميم")
    sender_name = await ment(sender)
    delpoints(event.sender_id, chat_id, points, 1000000)
    caption = f"تم تقييد {target_name} لمدة 30 ثانية. \n بطلب من {sender_name} \n\n **ملاحظة:** تم خصم 1000000 دينار من ثروتك."
    await ABH.send_file(chat_id, "https://t.me/VIPABH/592", caption=caption)
restriction_end_times = {}
@ABH.on(events.NewMessage(pattern='^تقييد عام|مخفي قيده|مخفي قيدة$'))
async def restrict_user(event):
    if not event.is_group:
        return
    # lock_key = f"lock:{event.chat_id}:تقييد"
    # x = redas.get(lock_key) == "True"
    # if not x:
    #     await chs(event, 'التقييد غير مفعل في هذه المجموعه🙄')
    #     return
    chat = await event.get_chat()
    chat_id = str(event.chat_id)
    user_id = event.sender_id
    if not is_assistant(chat_id, user_id):
        await notAssistantres(event)
        # await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")
    sender = await r.get_sender()
    name = await ment(sender)
    try:
        participant = await ABH(GetParticipantRequest(channel=chat, participant=sender.id))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return await event.reply(f"لا يمكنك تقييد {name} لانه مشرف ")
    except:
        return
    now = int(time.time())
    restriction_duration = 20 * 60
    user_to_restrict = await r.get_sender()
    user_id = user_to_restrict.id
    rights = ChatBannedRights(
        until_date=now + restriction_duration,
        send_messages=True
    )
    if event.chat_id in restriction_end_times and user_id in restriction_end_times[event.chat_id]:
        restriction_end_times[event.chat_id][user_id] = now + restriction_duration
        return
    try:
        await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
        type = "تقييد عام"
        await botuse(type)
        ء = await r.get_sender()
        rrr = await ment(ء)
        c = f"تم تقييد {rrr} لمدة 20 دقيقة."
        await ABH.send_file(event.chat_id, "https://t.me/VIPABH/592", caption=c)
        # خلي هنا ارسال رساله بقناة التبليغات
        await r.delete()
        await event.delete()
    except Exception as e:
        await hint(e)
        # خلي هنا شرط يتحقق من وجود صلاحيه المسح و شرط عدم وجودها مع تحديد سبب عدم حذف الرساله
        await event.reply(f" قيدته بس ماكدرت امسح الرساله ")
@ABH.on(events.NewMessage)
async def monitor_messages(event):
    if not event.is_group:
        return
    user_id = event.sender_id
    now = int(time.time())
    if event.chat_id in restriction_end_times and user_id in restriction_end_times[event.chat_id]:
        end_time = restriction_end_times[event.chat_id][user_id]
        if now < end_time:
            remaining = end_time - now
            try:
                chat = await event.get_chat()
                rights = ChatBannedRights(
                    until_date=now + remaining,
                    send_messages=True
                )
                await event.delete()
                await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
                rrr = await mention(event)
                c = f"تم اعاده تقييد {rrr} لمدة ** {remaining//60} دقيقة و {remaining%60} ثانية.**"
                await ABH.send_file(event.chat_id, "https://t.me/recoursec/15", caption=c)
                type = "تقييد مستخدمين"
                await botuse(type)
            except:
                pass
WHITELIST_FILE = "whitelist.json"
whitelist_lock = asyncio.Lock()
async def ads(group_id: int, user_id: int) -> None:
    async with whitelist_lock:
        data = {}
        if os.path.exists(WHITELIST_FILE):
            try:
                with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        group_key = str(group_id)
        group_list = data.get(group_key, [])
        if user_id not in group_list:
            group_list.append(user_id)
            data[group_key] = group_list
            with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
async def lw(group_id: int) -> list[int]:
    async with whitelist_lock:
        if not os.path.exists(WHITELIST_FILE):
            return []
        try:
            with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []
        return data.get(str(group_id), [])
CONFIG_FILE = "vars.json"
config_lock = asyncio.Lock()
async def configc(group_id: int, hint_cid: int) -> None:
    async with config_lock:
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                config = {}
        config[str(group_id)] = {"hint_gid": int(hint_cid)}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
async def LC(group_id: int) -> int | None:
    async with config_lock:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                return None
            group_config = config.get(str(group_id))
            if group_config and "hint_gid" in group_config:
                return int(group_config["hint_gid"])
        return None
report_data = {}
@ABH.on(events.MessageEdited)
async def edited(event):
    if not event.is_group or not event.message.edit_date:
        return
    msg = event.message
    chat_id = event.chat_id
    has_media = msg.media
    has_document = msg.document
    chat_dest = await LC(chat_id)
    if not chat_dest:
        return
    has_url = any(isinstance(entity, MessageEntityUrl) for entity in (msg.entities or []))
    if not (has_media or has_document or has_url):
        return
    uid = event.sender_id
    perms = await ABH.get_permissions(chat_id, uid)
    if perms.is_admin:
        return
    whitelist = await lw(chat_id)
    if event.sender_id in whitelist:
        return
    chat_obj = await event.get_chat()
    mention_text = await mention(event)
    if getattr(chat_obj, "username", None):
        رابط = f"https://t.me/{chat_obj.username}/{event.id}"
    else:
        clean_id = str(chat_obj.id).replace("-100", "")
        رابط = f"https://t.me/c/{clean_id}/{event.id}"
    buttons = [
        [
            Button.inline(' نعم', data=f"yes:{uid}"),
            Button.inline(' لا', data=f"no:{uid}")
        ]
    ]
    date_posted = event.message.date.strftime('%Y-%m-%d %H:%M')
    date_edited = event.message.edit_date.strftime('%Y-%m-%d %H:%M')
    sent_msg = await ABH.send_message(
        int(chat_dest),
        f"""تم تعديل رسالة مشتبه بها:
المستخدم: {mention_text}  
[رابط الرسالة]({رابط})  
معرفه: `{uid}`
هل تعتقد أن هذه الرسالة تحتوي على تلغيم؟  
تاريخ النشر - {date_posted}
تاريخ التعديل - {date_edited}
""",
        buttons=buttons,
        link_preview=True
    )
    report_data[sent_msg.id] = (uid, رابط, mention_text, date_posted, date_edited)
    await asyncio.sleep(60)
    if uid in whitelist:
        await sent_msg.delete()
        return
@ABH.on(events.CallbackQuery(pattern=r'^yes:(\d+)$'))
async def yes_callback(event):
    try:
        msg = await event.get_message()
        uid, الرابط, mention_text, date_posted, date_edited = report_data.get(msg.id, (None, None, None, None, None))
        if uid and الرابط and mention_text:
            m = await mention(event)
            await event.edit(
                f"""تم تأكيد أن المستخدم {mention_text} ملغم.
                [رابط الرسالة]({الرابط})
                معرفه: `{uid}`
                تاريخ النشر - {date_posted}
                تاريخ التعديل - {date_edited}
                بواسطه {m}
    """)
        await event.answer(' تم تسجيل المستخدم كملغّم.')
    except Exception as e:
        await hint(e)
@ABH.on(events.CallbackQuery(pattern=r'^no:(\d+)$'))
async def no_callback(event):
    try:
        msg = await event.get_message()
        uid, الرابط, mention_text, date_posted, date_edited = report_data.get(msg.id, (None, None, None, None, None))
        if uid and الرابط and mention_text:
            m = await mention(event)
            await event.edit(
                f"""تم تجاهل التبليغ عن المستخدم {mention_text}.
                [رابط الرسالة]({الرابط})
                ايديه `{uid}`
                تاريخ النشر - {date_posted}
                تاريخ التعديل - {date_edited}
                بواسطه {m}
    """)
        await event.answer(f" تم تجاهل التبليغ عن المستخدم {uid}")
        await ads(group, uid)
    except Exception as e:
        await hint(e)
@ABH.on(events.NewMessage(pattern='اضف قناة التبليغات'))
async def add_hintchannel(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not (await is_owner(chat_id, user_id) or user_id == 1910015590 or not event.is_group or is_assistant(chat_id, user_id)):
        return
    s = await event.get_sender()
    type = "اضافة قناة التبليغات"
    await botuse(type)
    if not event.is_group:
        return await event.reply("↯︙يجب تنفيذ هذا الأمر داخل مجموعة.")
    r = await event.get_reply_message()
    if not r:
        return await event.reply("↯︙يجب الرد على رسالة تحتوي على معرف القناة مثل -100xxxxxxxxxx")
    cid_text = r.raw_text.strip()
    if cid_text.startswith("-100") and cid_text[4:].isdigit():
        await configc(chat_id, cid_text)
        await event.reply(f"︙تم حفظ قناة التبليغات لهذه المجموعة")
        n = await ment(s)
        await ABH.send_message(int(cid_text), f'تم تعيين المحادثة الحاليه سجل ل بوت مخفي بواسطة ( {n} ) \n ايديه `{user_id}`')
    else:
        await event.reply("︙المعرف غير صالح، تأكد أنه يبدأ بـ -100 ويتكون من أرقام فقط.")
@ABH.on(events.NewMessage(pattern='اعرض قناة التبليغات'))
async def show_hintchannel(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not (await is_owner(chat_id, user_id) or user_id == 1910015590 or not event.is_group or is_assistant(chat_id, user_id)):
        return
    type = "عرض قناة التبليغات"
    await botuse(type)
    chat_id = event.chat_id
    c = await LC(chat_id)
    if c:
        await event.reply(f"︙قناة التبليغات لهذه المجموعة هي:\n`{c}`")
    else:
        await event.reply("︙لم يتم تعيين قناة تبليغات لهذه المجموعة بعد.")
banned_words = [
    "كمبي", "كوم بي", "قوم بي", "قم بي", "قوم به", "كومت", "قومت", "الطيازه", "دوده", 'دودة',
    "احط رجلي", "عاهرات", "عواهر", "عاهره", "عاهرة", "ناكك", "اشتعل دينه", "احترك دينك",
    "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", "برابيك", "نيجني", "العريض",
    "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", "خربدينه", "خربدينك", 
    "خرب بربك", "خربربج", "خربربها", "خرب بربها", "خرب بربة", "خرب بربكم", "كومبي", 
    "ارقة جاي", "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "كسين"
    "عيورتكم", "انيجة", "انيچة", "انيجه", "انيچه", "أناج", "اناج", "انيج", "أنيج", 
    "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", "كس", "عير", "كسمك", "كسختك", 
    "اتنيج", "ينيج", "طيرك", "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", 
    "خربدينة", "خربدينج", "خربدينكم", "خربدينها", "خربربه", "خربربة", "خربربك", 
    "خرب دينه", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", 
    "فريخ", "فريخة", "فريخه", "فرخي", "قضيب", "مايا", "ماية", "مايه", "بكسمك", 
    "كس امك", "طيز", "طيزك", "فرخ", "كواد", "اخلكحبة", "اينيج", "بربوك", "زب", 
    "الفرخ", "تيز", "كسم", "سكسي", "كحاب", "مناويج", "منيوج", "عيورة",
]
def normalize_arabic(text):
    text = re.sub(r'[\u064B-\u0652\u0640]', '', text)
    replace_map = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ى': 'ي',
        'ؤ': 'و',
        'ئ': 'ي',
        'ة': 'ه',
    }
    for src, target in replace_map.items():
        text = text.replace(src, target)    
    text = re.sub(r'(.)\1+', r'\1', text)    
    return text
normalized_banned_words = set(normalize_arabic(word) for word in banned_words)
async def is_admin(chat, user_id):
    try:
        participant = await ABH(GetParticipantRequest(chat, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False
def contains_banned_word(message):
    message = normalize_arabic(message)
    words = message.split()
    for word in words:
        if word in normalized_banned_words:
            return word
    return None
WARN_FILE = "warns.json"
def load_warns():
    if os.path.exists(WARN_FILE):
        with open(WARN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}
def save_warns(warns_data):
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(warns_data, f, ensure_ascii=False, indent=2)
def add_warning(user_id: int, chat_id: int) -> int:
    warns = load_warns()
    user_id_str = str(user_id)
    chat_id_str = str(chat_id)
    if user_id_str not in warns:
        warns[user_id_str] = {}
    if chat_id_str not in warns[user_id_str]:
        warns[user_id_str][chat_id_str] = 0
    warns[user_id_str][chat_id_str] += 1
    current_warns = warns[user_id_str][chat_id_str]
    if current_warns >= 3:
        warns[user_id_str][chat_id_str] = 0
        save_warns(warns)
    save_warns(warns)
    return current_warns
@ABH.on(events.NewMessage)
async def handler_res(event):
    lock_key = f"lock:{event.chat_id}:تقييد"
    x = redas.get(lock_key) == "True"
    if not event.is_group or not event.raw_text or not x:
        return
    message_text = event.raw_text.strip()
    x = contains_banned_word(message_text)
    user_id = event.sender_id
    chat = event.chat_id
    if x:
        if await is_admin(chat, user_id):
            await event.delete()
            return
        await event.delete()
        w = add_warning(user_id, chat)
        await botuse("تحذير مستخدمين")
        s = await mention(event)
        if w == 3:
            hint_channel = await LC(chat)
            if hint_channel:
                await ABH.send_message(
                    int(hint_channel),
                    f"""🔒 تم تقييد المستخدم
                👤 {s}
                ❗️بسبب تكرار استخدام كلمات محظورة.
                 سيتم رفع التقييد تلقائيًا بعد 20 دقيقة.
                 عدد التحذيرات: {w} / 3
                """
            )
            now = int(time.time())
            restriction_duration = 20 * 60
            restriction_end_times[event.chat_id][user_id] = now + restriction_duration
            rights = ChatBannedRights(
                until_date=now + restriction_duration,
                send_messages=True
            )     
            await ABH(EditBannedRequest(channel=chat, participant=user_id, banned_rights=rights))
        else:
            hint_channel = await LC(chat)
            await ABH.send_message(
                int(hint_channel),
                f"""كلمة محظورة!
            👤 من: {s}
            🆔 ايديه: `{user_id}`
            ❗ الكلمة المحظورة: `{x}`
             تم حذف الرسالة وتحذيره.
             عدد التحذيرات: {w} / 3
            """
            )
            type = "تقييد بسبب الفشار"
            await botuse(type)
@ABH.on(events.NewMessage(pattern='^تحذير$'))
async def warn_user(event):
    if not event.is_group:
        return
    chat_id = event.chat_id
    user_id = event.sender_id
    if not is_assistant(chat_id, user_id):
        return
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تحذيره.")
    target_id = r.sender_id
    if is_admin(chat_id, target_id) or is_assistant(chat_id, target_id):
        return await event.reply("لا يمكنك تحذير المشرفين أو المساعدين.")
    await event.delete()
    await r.delete()
    w = add_warning(target_id, chat_id)
    p = await r.get_sender()
    x = await mention(p)
    await event.respond(
        f"🚨 تم تحذير المستخدم:\n"
        f"👤 الاسم: {x}\n"
        f"🆔 الايدي: `{target_id}`\n"
        f"⚠️ عدد التحذيرات: {w} / 3"
    )
@ABH.on(events.NewMessage(pattern='!تجربة'))
async def test_broadcast(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    if not is_assistant(chat_id, user_id) or not event.is_group:
        return
    type = "تجربة"
    await botuse(type)
    hint_channel = await LC(chat_id)
    if not hint_channel:
        return await event.reply("↯︙لم يتم تعيين قناة تبليغات لهذه المجموعة بعد. استخدم الأمر 'اضف قناة التبليغات' أولاً.")
    try:
        hint_channel_id = int(hint_channel)
        await ABH.send_message(hint_channel_id, f"هذه رسالة تجربة من المجموعة: {chat_id}")
        await event.reply("✔︙تم إرسال رسالة التجربة إلى قناة التبليغات بنجاح.")
    except Exception as e:
        await event.reply(f"︙حدث خطأ أثناء إرسال الرسالة: {e}")
