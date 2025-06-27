from telethon.tl.functions.channels import  GetParticipantRequest
from telethon.tl.types import KeyboardButtonCallback
from db import save_date, get_saved_date #type: ignore
from ABH import ABH, events #type: ignore
from datetime import datetime, timedelta
from hijri_converter import Gregorian
from googletrans import Translator
from telethon import Button
from ABH import ABH, events
from other import botuse
@ABH.on(events.NewMessage(pattern='^/dates|مواعيد$'))
async def show_dates(event):
    if not event.is_group:
        return
    global uid, msg
    type = "مواعيد"
    await botuse(type)
    btton = [[
        Button.inline("محرم", b"m"),
        Button.inline("رمضان", b"rm"),
        Button.inline("شعبان", b"sh"),
        Button.inline("رجب", b"r"),
        Button.inline("حدد تاريخ", b"set_date")
    ]]
    msg = await event.respond("اختر الشهر المناسب أو حدد تاريخ خاص 👇", buttons=btton, reply_to=event.id)
    uid = event.sender_id
@ABH.on(events.CallbackQuery(data='set_date'))
async def set_date(event):
    المرسل_الثاني = event.sender_id
    if المرسل_الثاني != uid:
        await event.answer('عزيزي الامر لا يخصك', alert=True)
        return
    await event.edit("من فضلك أدخل التاريخ بصيغة YYYY-MM-DD مثال: 2025-06-15", buttons=None)
@ABH.on(events.CallbackQuery(data='m'))
async def handle_m(event):
    x = (2026, 6, 17)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await msg.edit(f'باقي {الباقي.days} لمحرم يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='rm'))
async def handle_rm(event):
    x = (2026, 2, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await msg.edit(f'باقي {الباقي.days} لرمضان يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='sh'))
async def handle_sh(event):
    x = (2026, 1, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await msg.edit(f'باقي {الباقي.days} لشعبان يوم', buttons=None)
@ABH.on(events.CallbackQuery(data='r'))
async def handle_r(event):
    x = (2025, 12, 22)
    الان = datetime.today()
    x_datetime = datetime(*x)
    الباقي = x_datetime - الان
    await msg.edit(f'باقي {الباقي.days} لرجب يوم', buttons=None)
@ABH.on(events.NewMessage(pattern=r'^\d{4}-\d{2}-\d{2}$'))
async def set_user_date(event):
    user_id = event.sender_id
    date = event.text
    try:
        datetime.strptime(date, "%Y-%m-%d")
        save_date(user_id, date)
        await event.reply(f"تم حفظ التاريخ {date}. يمكنك الآن معرفة كم باقي.")
    except ValueError:
        await event.reply("التاريخ المدخل غير صالح، يرجى إدخاله بصيغة YYYY-MM-DD.")
@ABH.on(events.NewMessage(pattern='^كم باقي$'))
async def check_remaining_days(event):
    if not event.is_group:
        return
    type = "كم باقي"
    await botuse(type)
    user_id = event.sender_id
    saved_date = get_saved_date(user_id)
    if saved_date:
        t = datetime.today()
        saved_date_obj = datetime.strptime(saved_date, "%Y-%m-%d").date()
        days_difference = (saved_date_obj - t.date()).days
        msg = f"باقي {days_difference} ايام" if days_difference >= 0 else f"التاريخ قد مضى منذ {abs(days_difference)} يوم"
        await event.reply(msg)
    else:
        await event.reply("لم تحدد تاريخًا بعد، يرجى تحديد تاريخ أولاً.")
@ABH.on(events.NewMessage(pattern='^تاريخ$'))
async def today(event):
    if not event.is_group:
        return
    type = "تاريخ"
    await botuse(type)
    tt = datetime.now().date()
    tt_minus_one = tt - timedelta(days=1)
    hd = Gregorian(tt_minus_one.year, tt_minus_one.month, tt_minus_one.day).to_hijri()
    hd_str = f"{hd.day} {hd.month_name('ar')} {hd.year} هـ"
    await event.reply(f"الهجري: \n{hd_str} \nالميلادي: \n{tt}")
@ABH.on(events.NewMessage(pattern=r'كشف ايدي (\d+)'))
async def link(event):
    if not event.is_group:
        return
    type = "كشف ايدي"
    await botuse(type)
    global user
    uid = event.sender_id
    user_id = event.pattern_match.group(1)
    if not user_id:
        await event.reply("استخدم الأمر كـ `كشف ايدي 1910015590`")
        return
    try:
        user = await event.client.get_entity(int(user_id))
    except Exception as e:
        return await event.reply(f"لا يوجد حساب بهذا الآيدي...")
    tag = user.first_name if user.first_name else '....'
    button = KeyboardButtonCallback("تغيير الئ رابط", b"recgange")
    await event.reply(f"⌔︙[{tag}](tg://user?id={user.id})", buttons=[button])
@ABH.on(events.CallbackQuery(data=b"recgange"))
async def chang(event):
    global user
    sender_id = event.sender_id 
    if sender_id != user.id:
        await event.answer("شلون وي الحشريين احنة \n عزيزي الامر خاص بالمرسل هوه يكدر يغير فقط😏", alert=True)
        return
    if uid is not None and sender_id == uid:
        await event.edit(f"⌔︙رابط المستخدم: tg://user?id={user.id}")
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def translation(event):
    if not event.is_group:
        return
    type = "ترجمة"
    await botuse(type)
    translator = Translator()
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        
        return
    detected_language = await translator.detect(original_text)
    if detected_language.lang == "ar": 
        translated = await translator.translate(original_text, dest="en")
    else: 
        translated = await translator.translate(original_text, dest="ar")
    response = (
        f"اللغة المكتشفة: {detected_language.lang}\n"
        f"النص المترجم: `{translated.text}`"
    )
    await event.reply(response)
rights_translation = {
    "change_info": "تغيير معلومات المجموعة",
    "ban_users": "حظر الأعضاء",
    "invite_users": "دعوة أعضاء",
    "pin_messages": "تثبيت الرسائل",
    "add_admins": "إضافة مشرفين",
    "manage_call": "إدارة المكالمات الصوتية",
    "anonymous": "الوضع المتخفي",
    "manage_topics": "إدارة المواضيع",
}
def translate_rights_lines(rights_obj):
    lines = []
    for key, name in rights_translation.items():
        status = getattr(rights_obj, key, False)
        emoji = "👍🏾" if status else "👎🏾"
        lines.append(f"{emoji} ⇜ {name}")
    return "\n".join(lines) if lines else "لا يوجد صلاحيات"
@ABH.on(events.NewMessage(pattern=r'^صلاحياته(?: (.+))?$'))
async def his_rights(event):
    if not event.is_group:
        return
    type = "صلاحياته"
    await botuse(type)
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        translated = translate_rights_lines(result.participant.admin_rights)
        await event.reply(f"صلاحياته\n{translated}")
    except Exception:
        await event.reply("لا يمكن عرض الصلاحيات.")
@ABH.on(events.NewMessage(pattern=r'^لقبه(?: (.+))?$'))
async def nickname_r(event):
    if not event.is_group:
        return
    type = "لقبه"
    await botuse(type)
    try:
        chat = await event.get_input_chat()
        match = event.pattern_match.group(1)
        if match:
            target = match
        else:
            reply = await event.get_reply_message()
            if not reply:
                await event.reply("استخدم الرد على رسالة المستخدم أو أرسل معرفه بعد الأمر.")
                return
            target = reply.sender_id
        result = await ABH(GetParticipantRequest(channel=chat, participant=target))
        participant = result.participant
        nickname = getattr(participant, 'rank', None) or "مشرف"
        await event.reply(f"لقبه ↞ {nickname}")
    except Exception:
        await event.reply("المستخدم ليس مشرفًا أو لا يمكن العثور عليه.")
