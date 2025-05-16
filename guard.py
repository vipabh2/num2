from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, MessageEntityUrl
from Resources import group, mention
from telethon import events, Button
from ABH import ABH
import asyncio, re
import json
import os
import os
import json
import asyncio
def load_whitelist():
    try:
        with open("whitelist.json", "r") as f:
            return json.load(f)["whitelist"]
    except FileNotFoundError:
        return []
def save_whitelist(data):
    with open("whitelist.json", "w") as f:
        json.dump({"whitelist": data}, f, indent=2)
CONFIG_FILE = "vars.json"
config_lock = asyncio.Lock()
async def configc(group_id, hint_cid):
    async with config_lock:
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                config = {}
        config[str(group_id)] = {"hint_gid": hint_cid}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
async def LC(group_id):
    async with config_lock: 
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                return None
            group_config = config.get(str(group_id))
            if group_config:
                return group_config.get("hint_gid")
        return None
@ABH.on(events.NewMessage(pattern='اضف قناة التبليغات'))
async def add_hintchannel(event):
    if not event.is_group:
        return await event.reply("↯︙يجب تنفيذ هذا الأمر داخل مجموعة.")
    
    r = await event.get_reply_message()
    if not r:
        return await event.reply("↯︙يجب الرد على رسالة تحتوي على معرف القناة مثل -100xxxxxxxxxx")
    
    cid_text = r.raw_text.strip()
    if cid_text.startswith("-100") and cid_text[4:].isdigit():
        chat_id = event.chat_id
        await configc(chat_id, cid_text)
        await event.reply(f"︙تم حفظ قناة التبليغات لهذه المجموعة:\n`{cid_text}`")
    else:
        await event.reply("︙المعرف غير صالح، تأكد أنه يبدأ بـ -100 ويتكون من أرقام فقط.")
@ABH.on(events.NewMessage(pattern='اعرض قناة التبليغات'))
async def show_hintchannel(event):
    chat_id = event.chat_id
    c = await LC(chat_id)
    if c:
        await event.reply(f"︙قناة التبليغات لهذه المجموعة هي:\n`{c}`")
    else:
        await event.reply("︙لم يتم تعيين قناة تبليغات لهذه المجموعة بعد.")
@ABH.on(events.MessageEdited)
async def edited(event):
    msg = event.message
    chat = event.chat_id
    if chat != group or not msg.edit_date:
        return
    has_media = bool(msg.media)
    has_document = bool(msg.document)
    has_url = any(isinstance(entity, MessageEntityUrl) for entity in (msg.entities or []))
    if not (has_media or has_document or has_url):
        return
    uid = event.sender_id
    whitelist = load_whitelist()
    if uid in whitelist:
        return
    perms = await ABH.get_permissions(chat, uid)
    if perms.is_admin:
        return
    if uid not in load_whitelist():
        c = event.chat_id
        s = await event.get_sender()
        m = await mention(event, s)
        HID = int(str(await LC(c)))
        chat_id = await LC(c)
        i = str(chat_id).replace("-100", "")
        ch = i.replace("-100", "")
        الرابط = f"http://t.me/c/{ch}/{event.id}"
        b = [Button.inline('نعم', data='yes'), Button.inline('لا', data='no')]
        await ABH.send_message(HID, f"""
    تم تعديل رسالة من {m}

    الرابط ⇠ ( {الرابط} )

    ايديه ⇠ {c.id}
    هل كان هذا تلغيم؟
    """, Button=b)
        await asyncio.sleep(60)
        await event.delete()
banned_words = [
    "احط رجلي", "عاهرات", "عواهر", "عاهره", "عاهرة", "ناكك", "اشتعل دينه", "احترك دينك",
    "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", "خربدينه", "خربدينك", 
    "خرب بربك", "خربربج", "خربربها", "خرب بربها", "خرب بربة", "خرب بربكم", "كومبي", 
    "عيورتكم", "انيجة", "انيچة", "انيجه", "انيچه", "أناج", "اناج", "انيج", "أنيج", 
    "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", "كس", "عير", "كسمك", "كسختك", 
    "اتنيج", "ينيج", "طيرك", "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", 
    "خربدينة", "خربدينج", "خربدينكم", "خربدينها", "خربربه", "خربربة", "خربربك", 
    "الفرخ", "الفرحْ", "تيز", "كسم", "سكسي", "كحاب", "مناويج", "منيوج", "عيورة", 
    "خرب دينه", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", 
    "فريخ", "فريخة", "فريخه", "فرخي", "قضيب", "مايا", "ماية", "مايه", "بكسمك", 
    "كس امك", "طيز", "طيزك", "فرخ", "كواد", "اخلكحبة", "اينيج", "بربوك", "زب", 
    "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", "برابيك", "نيجني", 
    "كمبي", "كوم بي", "قوم بي", "قم بي", "قوم به", "كومت", "قومت", "الطيازه", 
    "ارقة جاي", "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "كسين", "سب"
]
def normalize_arabic(text):
    text = text.lower()
    text = re.sub(r'[ًٌٍَُِّْـ]', '', text)
    replace_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي', 'ة': 'ه'}
    for old, new in replace_map.items():
        text = text.replace(old, new)
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
    message_text = event.raw_text.strip()
    if contains_banned_word(message_text):
        user_id = event.sender_id
        chat = await event.get_chat()
        if await is_admin(chat, user_id):
            await event.delete()
            return
        await event.delete()
        if user_id not in warns:
            warns[user_id] = {}
        if chat.id not in warns[user_id]:
            warns[user_id][chat.id] = 0
        warns[user_id][chat.id] += 1
        if warns[user_id][chat.id] >= 2:
            await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
            sender = await event.get_sender()
            name = await mention(event, sender)
            warns[user_id][chat.id] = 0
            hint_channel = await LC(chat.id)
            if hint_channel:
                try:
                    await ABH.send_message(int(hint_channel), f'تم تقييد المستخدم {name}')
                except:
                    pass
            await asyncio.sleep(1200)
            await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))
@ABH.on(events.NewMessage(pattern='!تجربة'))
async def test_broadcast(event):
    if not event.is_group:
        return await event.reply("↯︙هذا الأمر يعمل فقط داخل المجموعات.")
    
    chat_id = event.chat_id
    hint_channel = await LC(chat_id)
    
    if not hint_channel:
        return await event.reply("↯︙لم يتم تعيين قناة تبليغات لهذه المجموعة بعد. استخدم الأمر 'اضف قناة التبليغات' أولاً.")
    try:
        hint_channel_id = int(hint_channel)
        await ABH.send_message(hint_channel_id, f"هذه رسالة تجربة من المجموعة: {chat_id}")
        await event.reply("✔︙تم إرسال رسالة التجربة إلى قناة التبليغات بنجاح.")
    except Exception as e:
        await event.reply(f"︙حدث خطأ أثناء إرسال الرسالة: {e}")
