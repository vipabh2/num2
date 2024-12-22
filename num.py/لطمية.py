import telebot
from telebot import types
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import time
import random
import os

bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)


basimurl = (
    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
    "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
    "70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
    "80", "81", "82", "83", "84", "85", "86", "87", "88", "89",
    "90", "91", "92", "93", "94", "95", "96", "97", "98", "99",
    "100", "101", "102", "103", "104", "105", "106", "107", "108", "109",
    "110", "111", "112", "113", "114", "115", "116", "117", "118"
)
mohmurl = (
    "119", "120", "121", "122", "123", "124", "125", "126", "127", "128",
    "129", "130", "131", "132", "133", "134", "135", "136", "137", "138"
)

musurl = ('139', '140', '141', '142', '143', '144', '145', '146', '147',
            '148', '149', '150', '151', '152', '153', '154'
            )

nurl = ('164', '165', '166', '167', '168', '169', '170')

furl = ('171', '172', '173', '174')




@bot.message_handler(func=lambda message: message.text in ['لطمية'] or message.text in ['لطميه'])
def vipabh(message):
    current_time = datetime.now()
    message_time = datetime.fromtimestamp(message.date) 
    time_difference = (current_time - message_time).total_seconds()
    if time_difference > 20:
        return 
    username = message.from_user.username if message.from_user.username else "لا يوجد اسم مستخدم"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("باسم", callback_data="باسم"))
    markup.add(types.InlineKeyboardButton("الخاقاني", callback_data="الخاقاني"))
    markup.add(types.InlineKeyboardButton("مسلم", callback_data="مسلم"))
    markup.add(types.InlineKeyboardButton("نزلة", callback_data="نزلة"))
    markup.add(types.InlineKeyboardButton("فاقد", callback_data="فاقد"))
    bot.send_video(
        message.chat.id,
        "https://t.me/VIPABH/1212",  
        caption=f"اهلا [{message.from_user.first_name}](https://t.me/{username}) حياك الله! اضغط على الرادود.",
        parse_mode="Markdown",
        reply_markup=markup
    )


def send_audio_from_f_list(call):
    rl = random.choice(furl)  
    audio_url = f"https://t.me/sossosic/{rl}"  
    
    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        # caption=f"{audio_url}", 
        caption="᯽︙اذكر القائم",
        parse_mode="html"
    )

def send_audio_from_n_list(call):
    rl = random.choice(nurl)  
    audio_url = f"https://t.me/sossosic/{rl}"  
    
    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        # caption=f"{audio_url}", 
        caption="᯽︙اذكر القائم",
        parse_mode="html"
    )


def send_audio_from_basim_list(call):
    rl = random.choice(furl)  
    audio_url = f"https://t.me/sossosic/{rl}"  
    
    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        # caption=f"{audio_url}", 
        caption="᯽︙اذكر القائم",
        parse_mode="html"
    )

def send_audio_from_mohmurl_list(call):
    rl = random.choice(mohmurl)  
    audio_url = f"https://t.me/sossosic/{rl}"  
    
    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        # caption=f"{audio_url}", 
        caption="᯽︙اذكر القائم",
        parse_mode="html"
    )

def send_audio_from_mus_list(call):
    rl = random.choice(musurl) 
    audio_url = f"https://t.me/sossosic/{rl}" 

    bot.send_audio(
        chat_id=call.message.chat.id,
        audio=audio_url,
        caption="᯽︙اذكر القائم",
        # caption=f"{audio_url}", 
        parse_mode="html"
    )

@bot.callback_query_handler(func=lambda call: call.data == "باسم")
def send_basim(call):
    send_audio_from_basim_list(call)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
        )
@bot.callback_query_handler(func=lambda call: call.data == "الخاقاني")
def send_khaqani(call):
    send_audio_from_mohmurl_list(call)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
        )
@bot.callback_query_handler(func=lambda call: call.data == "مسلم")
def send_mus(call):
    send_audio_from_mus_list(call)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
        )
@bot.callback_query_handler(func=lambda call: call.data == "نزلة")
def send_mus(call):
    send_audio_from_n_list(call)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
        )

@bot.callback_query_handler(func=lambda call: call.data == "فاقد")
def send_mus(call):
    send_audio_from_f_list(call)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
        )

    
if __name__ == "__main__":
    bot.polling(none_stop=True)
