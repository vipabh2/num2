from telethon.tl.functions.channels import  GetParticipantRequest
import google.generativeai as genai
from ABH import ABH, events #type: ignore
import  pytz
timezone = pytz.timezone('Asia/Baghdad')
GEMINI = "AIzaSyA5pzOpKVcMGm6Aek82KoB3Pk94dYg3LX4"
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel("gemini-1.5-flash")
group = -1001784332159
hint_gid = -1002168230471
bot = "Anymous"
wfffp = 1910015590
rights_translation = {
    "change_info": "تغيير معلومات المجموعة",
    "post_messages": "نشر الرسائل",
    "edit_messages": "تعديل الرسائل",
    "delete_messages": "حذف الرسائل",
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
      
