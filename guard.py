from telethon.tl.types import MessageEntityUrl
from Resources import hint_gid 
from Resources import group
from ABH import ABH, events
import asyncio, re
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
    "ارقة جاي", "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "كسين"
]
set_Bwords = {word: re.sub(r'(.)\1+', r'\1', word) for word in banned_words}
def normalize_text(text):
 text = text.lower()
 text = re.sub(r'[^أ-يa-zA-Z\s]', '', text)
 replace_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي'}
 for old, new in replace_map.items():
  text = text.replace(old, new)
 text = re.sub(r'(.)\1+', r'\1', text)
 return text
async def is_admin(chat, user_id):
 try:
  participant = await ABH(GetParticipantRequest(chat, user_id))
  return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
 except:
  return False
def check_message(message):
 normalized_message = normalize_text(message)
 words = normalized_message.split()
 return any(word in set_Bwords.values() for word in words)
restrict_rights = ChatBannedRights(until_date=None,send_messages=True,send_media=True,send_stickers=True,send_gifs=True,send_games=True,send_inline=True,embed_links=True)
unrestrict_rights = ChatBannedRights(until_date=None,send_messages=False,send_media=False,send_stickers=False,send_gifs=False,send_games=False,send_inline=False,embed_links=False)
warns = {}
@ABH.on(events.NewMessage)
async def handler_res(event):
 if event.is_group:
  message_text = event.raw_text.strip()
  if check_message(message_text):  
   user_id = event.sender_id
   chat = await event.get_chat()
   if await is_admin(chat, user_id):
    await event.delete()
    return
   if user_id not in warns:
    warns[user_id] = {}
   if chat.id not in warns[user_id]:
    warns[user_id][chat.id] = 0
   warns[user_id][chat.id] += 1
   msg = event.message
   await msg.delete()
   if warns[user_id][chat.id] == 2:
    await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
    sender = await event.get_sender()
    name = sender.first_name
    await ABH.send_message(hint_gid, f'تم تقييد المستخدم {name} \n بواسطة {bot}')
    warns[user_id][chat.id] = 0
    await asyncio.sleep(20 * 60)
    await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))
