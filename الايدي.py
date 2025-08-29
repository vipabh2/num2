from telethon.tl.types import Channel, ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipant
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.users import GetFullUserRequest
from datetime import datetime
import aiohttp, asyncio, os
from telethon import events
from Program import *
from other import *
from ABH import ABH
id_status_per_chat = {}
@ABH.on(events.NewMessage(pattern='الايدي (تفعيل|تعطيل)'))
async def turn(event):
    if not event.is_group:
        return
    chat_id = event.chat_id
    id = event.sender_id
    isas = is_assistant(chat_id, id)
    dev = save(None, 'assistant.json')
    owner = await get_owner(event)
    print(f"User ID: {id}, Is Assistant: {isas}, Is Owner: {wfffp == owner.id} isdev {id in dev}")
    if not (id == wfffp or not isas or id in dev or id == owner):
        return
LOCAL_PHOTO_DIR = "photos"
os.makedirs(LOCAL_PHOTO_DIR, exist_ok=True)
async def get_user_role(user_id, chat_id):
    try:
        chat = await ABH.get_entity(chat_id)
        if isinstance(chat, Channel):
            result = await ABH(GetParticipantRequest(channel=chat, participant=user_id))
            participant = result.participant
            if isinstance(participant, ChannelParticipantCreator):
                return "مالك"
            elif isinstance(participant, ChannelParticipantAdmin):
                return "مشرف"
            elif isinstance(participant, ChannelParticipant):
                return "عضو"
            else:
                return ''
        else:
            return ''
    except Exception:
        return "🌚"
async def date(user_id):
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    async with aiohttp.ClientSession() as session:
        async with session.post('https://restore-access.indream.app/regdate', headers=headers, data=data) as response:
            if response.status == 200:
                response_json = await response.json()
                date_string = response_json['data']['date']
                try:
                    if len(date_string.split("-")) == 3:
                        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%Y/%m/%d")
                    else:
                        date_obj = datetime.strptime(date_string, "%Y-%m")
                        formatted_date = date_obj.strftime("%Y/%m")
                    return formatted_date
                except Exception:
                    return "تاريخ غير صالح"
            else:
                return "غير معروف"
LOCAL_PHOTO_DIR = "/tmp"
@ABH.on(events.NewMessage(pattern='^(id|اا|افتار)$', from_users=wfffp))
async def hisid(event):
    if not event.is_group:
        return
    chat_id = event.chat_id
    replied_message = await event.get_reply_message()
    if not replied_message:
        return
    type = "id"
    await botuse(type)
    sender_id = replied_message.sender_id
    user = await ABH.get_entity(sender_id)
    user_id = user.id
    chat_id = event.chat_id
    phone = user.phone if hasattr(user, 'phone') and user.phone else "👎"
    premium = "yes" if user.premium else "no"
    usernames = [f"@{username.username}" for username in user.usernames] if user.usernames else [f"@{user.username}"] if user.username else ["—"]
    usernames_list = ", ".join(usernames)
    dates = await date(user_id)
    states = await get_user_role(user_id, chat_id)
    FullUser = (await event.client(GetFullUserRequest(user.id))).full_user
    bio = FullUser.about
    bio_text = f"\n{bio}" if bio and bio.strip() else ""
    year = int(dates.split("/")[0])
    if year < 2016:
        x = "انت من جماعة الباند؟؟"
    elif 2016 <= year < 2023:
        x = "لا بأس"
    else:
        x = "جديد"
    message_text = (
        f"⌯ اليوزر ⇠ {usernames_list}\n"
        f"⌯ الرقم  {'+' + phone if phone != '—' else phone}\n"
        f"⌯ غني ام فقير ⇠ {premium}\n"
        f"⌯ الانشاء ⇠ {dates} {x}\n"
        f"⌯ رتبتك بالمجموعة ⇠ {states}"
        f"{bio_text}"
    )
    if user.photo:
        photo_path = os.path.join(LOCAL_PHOTO_DIR, f"{user_id}.jpg")
        await ABH.download_profile_photo(user.id, file=photo_path)
        msg = await ABH.send_file(event.chat_id, photo_path, caption=message_text, force_document=False, reply_to=event.message.id)
        await asyncio.sleep(60*3)
        await msg.delete()
    else:
        await event.respond(message_text, reply_to=event.message.id)
@ABH.on(events.NewMessage(pattern=r"^(id|ايدي|افتاري|ا|\.)$", from_users=wfffp))
async def myid(event):
    if not event.is_group:
        return
    chat_id = event.chat_id
    type = "reply id"
    await botuse(type)
    sender_id = event.sender_id
    user = await ABH.get_entity(sender_id)
    user_id = user.id
    chat_id = event.chat_id
    phone = user.phone if hasattr(user, 'phone') and user.phone else "غير متوفر💔"
    premium = "عنده مميز" if user.premium else "ماعنده مميز"
    usernames = [f"@{username.username}" for username in user.usernames] if user.usernames else [f"@{user.username}"] if user.username else ["—"]
    usernames_list = ", ".join(usernames)
    dates = await date(user_id)
    states = await get_user_role(user_id, chat_id)
    FullUser = (await event.client(GetFullUserRequest(user.id))).full_user
    bio = FullUser.about
    bio_text = f"\n{bio}" if bio and bio.strip() else ""
    year = int(dates.split("/")[0])
    if year < 2016:
        x = "انت من جماعة الباند؟؟"
    elif 2016 <= year < 2023:
        x = "لا بأس"
    else:
        x = "جديد"
    message_text = (
        f"⌯ اليوزر ⇠ {usernames_list}\n"
        f"⌯ الرقم  {'+' + phone if phone != '—' else phone}\n"
        f"⌯ غني ام فقير ⇠ {premium}\n"
        f"⌯ الانشاء ⇠ {dates} {x}\n"
        f"⌯ رتبتك بالمجموعة ⇠ {states}"
        f"{bio_text}"
    )
    if user.photo:
        photo_path = os.path.join(LOCAL_PHOTO_DIR, f"{user_id}.jpg")
        await ABH.download_profile_photo(user.id, file=photo_path)
        msg = await ABH.send_file(event.chat_id, photo_path, caption=message_text, force_document=False, reply_to=event.message.id)
        await asyncio.sleep(60*3)
        await msg.delete()
    else:
        await event.respond(message_text, reply_to=event.message.id)
