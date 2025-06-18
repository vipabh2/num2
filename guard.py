from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, MessageEntityUrl
from other import is_assistant, botuse
from Resources import group, mention, ment
from telethon import events, Button
import os, asyncio, re, json, time
from Program import r as redas, chs
from ABH import ABH
restriction_end_times = {}
@ABH.on(events.NewMessage(pattern=r"^التقييد (تفعيل|تعطيل)$"))
async def toggle_feature(event):
    if not event.is_group:
        return
    if not is_assistant(event.chat_id, event.sender_id):
        await chs(event, 'شني خالي كبينه انت مو معاون')
        return
    action = event.pattern_match.group(1)
    value = True if action == "تفعيل" else False
    type = f"{value} التقييد"
    await botuse(type)
    redas.hset(str(event.chat_id), 't', str(value))
    await event.reply(f"تم {action} التقييد تدلل حبيبي")
@ABH.on(events.NewMessage(pattern='^تقييد عام|مخفي قيده|مخفي قيدة$'))
async def restrict_user(event):
    if not event.is_group:
        return
    # if not islock(event.chat_id):
    status = redas.hget(str(event.chat_id), 't')
    if status != "True":
        await event.reply("هذه الميزة غير مفعلة في هذه المجموعة.")
        return
    chat = await event.get_chat()
    chat_id = str(event.chat_id)
    user_id = event.sender_id
    r = await event.get_reply_message()
    if not r:
        return await event.reply("يجب الرد على رسالة العضو الذي تريد تقييده.")
    sender = await r.get_sender()
    if not is_assistant(chat_id, user_id):
        await event.reply("جا قيدته الك بس انت مو معاون")
        return
    await r.delete()
    name = await ment(sender)
    try:
        participant = await ABH(GetParticipantRequest(channel=chat.id, participant=sender.id))
        if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return await event.reply(f"لا يمكنك تقييد {name} لانه مشرف ")
    except:
        return
    user_to_restrict = await r.get_sender()
    user_id = user_to_restrict.id
    now = int(time.time())
    restriction_duration = 20 * 60
    restriction_end_times[user_id] = now + restriction_duration
    rights = ChatBannedRights(
        until_date=now + restriction_duration,
        send_messages=True
    )      
    try:
        await ABH(EditBannedRequest(channel=chat.id, participant=user_id, banned_rights=rights))
        type = "تقييد عام"
        await botuse(type)
        ء = await r.get_sender()
        rrr = await ment(ء)
        c = f"تم تقييد {rrr} لمدة 20 دقيقة."
        await ABH.send_file(event.chat_id, "https://t.me/VIPABH/592", caption=c)
        await event.delete()
    except Exception as e:
        await event.reply(f" ياريت اقيده بس ماكدر {e}")
@ABH.on(events.NewMessage)
async def monitor_messages(event):
    if not event.is_group:
        return
    user_id = event.sender_id
    now = int(time.time())
    if user_id in restriction_end_times:
        end_time = restriction_end_times[user_id]
        if now < end_time:
            remaining = end_time - now
            try:
                chat = await event.get_chat()
                rights = ChatBannedRights(
                    until_date=now + remaining,
                    send_messages=True
                )
                await event.delete()
                await ABH(EditBannedRequest(channel=chat.id, participant=user_id, banned_rights=rights))
                ء = await event.get_sender()
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
    if not event.is_group:
        return
    msg = event.message
    chat_id = event.chat_id
    if chat_id != group or not msg.edit_date:
        return
    whitelist = await lw(chat_id)
    if event.sender_id in whitelist:
        return
    has_media = bool(msg.media)
    has_document = bool(msg.document)
    has_url = any(isinstance(entity, MessageEntityUrl) for entity in (msg.entities or []))
    if not (has_media or has_document or has_url):
        return
    uid = event.sender_id
    perms = await ABH.get_permissions(chat_id, uid)
    if perms.is_admin:
        return
    chat_dest = await LC(chat_id)
    if not chat_dest:
        await asyncio.sleep(60)
        await event.delete()
        return
    chat_obj = await event.get_chat()
    mention_text = await mention(event)
    if getattr(chat_obj, "username", None):
        رابط = f"https://t.me/{chat_obj.username}/{event.id}"
    else:
        clean_id = str(chat_obj.id).replace("-100", "")
        رابط = f"https://t.me/c/{clean_id}/{event.id}"
    report_data[event.id] = uid
    buttons = [
        [
            Button.inline(' نعم', data=f"yes:{uid}"),
            Button.inline(' لا', data=f"no:{uid}")
        ]
    ]
    await ABH.send_message(
        int(chat_dest),
        f""" تم تعديل رسالة مشتبه بها:
 المستخدم: {mention_text}  
 [رابط الرسالة]({رابط})  
 معرفه: `{uid}`
 هل تعتقد أن هذه الرسالة تحتوي على تلغيم؟""",
        buttons=buttons,
        link_preview=True
    )
    await asyncio.sleep(60)
    await event.delete()
@ABH.on(events.CallbackQuery(pattern=r'^yes:(\d+)$'))
async def yes_callback(event):
    uid = int(event.pattern_match.group(1))
    await event.answer(' تم تسجيل المستخدم كملغّم.')
@ABH.on(events.CallbackQuery(pattern=r'^no:(\d+)$'))
async def no_callback(event):
    uid = int(event.pattern_match.group(1))
    await event.answer(f" تم تجاهل التبليغ عن المستخدم {uid}")
    await ads(group, uid)
@ABH.on(events.NewMessage(pattern='اضف قناة التبليغات'))
async def add_hintchannel(event):
    if not event.is_group:
        return
    type = "اضافة قناة التبليغات"
    await botuse(type)
    if not event.is_group:
        return await event.reply("↯︙يجب تنفيذ هذا الأمر داخل مجموعة.")
    r = await event.get_reply_message()
    if not r:
        return await event.reply("↯︙يجب الرد على رسالة تحتوي على معرف القناة مثل -100xxxxxxxxxx")
    cid_text = r.raw_text.strip()
    if cid_text.startswith("-100") and cid_text[4:].isdigit():
        chat_id = event.chat_id
        await configc(chat_id, cid_text)
        await event.reply(f"︙تم حفظ قناة التبليغات لهذه المجموعة")
    else:
        await event.reply("︙المعرف غير صالح، تأكد أنه يبدأ بـ -100 ويتكون من أرقام فقط.")
@ABH.on(events.NewMessage(pattern='اعرض قناة التبليغات'))
async def show_hintchannel(event):
    if not event.is_group:
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
    "الفرخ", "الفرحْ", "تيز", "كسم", "سكسي", "كحاب", "مناويج", "منيوج", "عيورة", 
    "خرب دينه", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", 
    "فريخ", "فريخة", "فريخه", "فرخي", "قضيب", "مايا", "ماية", "مايه", "بكسمك", 
    "كس امك", "طيز", "طيزك", "فرخ", "كواد", "اخلكحبة", "اينيج", "بربوك", "زب", 
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
    return any(word in normalized_banned_words for word in words)
restrict_rights = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)
unrestrict_rights = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)
warns = {}
@ABH.on(events.NewMessage)
async def handler_res(event):
    if not event.is_group:
        return
    ء = redas.hget(str(event.chat_id), 't')
    if not ء or not event.is_group:
        return
    if event.message.action or not event.raw_text:
        return 
    message_text = event.raw_text.strip()
    x = contains_banned_word(message_text)
    if x:
        user_id = event.sender_id
        chat = await event.get_chat()
        if await is_admin(chat, user_id):
            await event.delete()
            return
        await event.delete()
        if chat.id not in warns:
            warns[chat.id] = {}
        if user_id not in warns[chat.id]:
            warns[chat.id][user_id] = 0
        warns[chat.id][user_id] += 1
        s = await mention(event)
        hint_channel = await LC(chat.id)
        await ABH.send_message(
            int(hint_channel),
            f'المستخدم ( {s} ) ارسل كلمة غير مرغوب بها ( {x} ) \n   ايديه ( `{user_id}` ) تم تحذيره ومسحها \n تحذيراته ( 3\{warns[chat.id][user_id]} ) '
            )
        type = "تقييد بسبب الفشار"
        await botuse(type)
        if warns[chat.id][user_id] >= 3:
            await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
            name = await mention(event)
            warns[chat.id][user_id] = 0
            hint_channel = await LC(chat.id)
            if hint_channel:
                await ABH.send_message(
                    int(hint_channel),
                    f'تم تقييد المستخدم {name} \n ارسل كلمه ممنوعه ( {x} )'
                        )
            await asyncio.sleep(1200)
            await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))
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
