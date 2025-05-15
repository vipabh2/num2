from telethon.tl.types import ChatBannedRights, MessageEntityUrl
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from Resources import group, mention
from telethon import events
from ABH import ABH
import asyncio, re
import json
import os
import os
import json
import asyncio

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
    if event.is_group:
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
            c = await LC(chat.id)
            if user_id in warns and chat.id in warns[user_id] and warns[user_id][chat.id] >= 2:
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                sender = await event.get_sender()
                name = await mention(event, sender)
                warns[user_id][chat.id] = 0
            if c:
                await ABH.send_message(int(c), f'تم تقييد المستخدم {name}')
                await asyncio.sleep(20 * 60)
                await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))
