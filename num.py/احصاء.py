from pyrogram.types import Message
from pyrogram import Client, filters
from StringSessionBot.database import SESSION
from StringSessionBot.database.users_sql import Users, num_users

@Client.on_message(~filters.service, group=1)
async def users_sql(_, msg: Message):
    if msg.from_user:
        try:
            q = SESSION.query(Users).get(int(msg.from_user.id))
            if not q:
                SESSION.add(Users(msg.from_user.id))
                SESSION.commit()
        except Exception as e:
            print(f"خطأ في إضافة المستخدم: {e}")
        finally:
            SESSION.close()

@Client.on_message(filters.user(705475246) & filters.command("احصاء"))
async def _stats(_, msg: Message):
    try:
        users = await num_users()
        await msg.reply(f"ᴛᴏᴛᴀʟ ᴜsᴇʀs : {users}", quote=True)
    except Exception as e:
        await msg.reply(f"حدث خطأ أثناء حساب عدد المستخدمين: {e}")
