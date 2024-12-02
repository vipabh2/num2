import random
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: message.text in ['لطميه', 'لطمية'])
def handle_message(message):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton("باسميات", callback_data="باسم"),
        InlineKeyboardButton("حيدر البياتي", callback_data="حيدر"),
        InlineKeyboardButton("الخاقاني", callback_data="فاقد"),
        InlineKeyboardButton("مسلم الوائلي", callback_data="مسلم"),
        InlineKeyboardButton("منوع", callback_data="منوع"),
        InlineKeyboardButton("مزيد من الخيارات", callback_data="مزيد")
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "اختر لطمية 🫀", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "مزيد")
def handle_more_options(call):
    markup = InlineKeyboardMarkup(row_width=3)
    more_buttons = [
        InlineKeyboardButton("نزلة", callback_data="نزلة"),
        InlineKeyboardButton("مصطفى السوداني", callback_data="مصطفى"),
        InlineKeyboardButton("افراح", callback_data="افراح"),
        InlineKeyboardButton("عشوائي", callback_data="عشوائي")
    ]
    markup.add(*more_buttons)
    bot.send_message(call.message.chat.id, "خيارات إضافية:", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "عشوائي":
            # إرسال ملف عشوائي
            rl = random.randint(157, 306)  
            url = f"https://t.me/iitt_5/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "باسم":
            # إرسال ملف عشوائي
            rl = random.randint(50, 118) 
            url = f"https://t.me/sossosic/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "فاقد":
            # إرسال ملف عشوائي
            rl = random.randint(5, 20) 
            url = f"https://t.me/F2_ie/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "حيدر":
            # إرسال ملف عشوائي
            rl = random.randint(7, 14) 
            url = f"https://t.me/leonil_messi10/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "مسلم":
            # إرسال ملف عشوائي
            rl = random.randint(51, 60) 
            url = f"https://t.me/sossosic/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "منوع":
            # إرسال ملف عشوائي
            rl = random.randint(50, 117) 
            url = f"https://t.me/sossosic/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

        elif call.data == "نزلة":
            # إرسال ملف عشوائي
            rl = random.randint(7, 12) 
            url = f"https://t.me/x04uc/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

            
        elif call.data == "مصطفى":
            # إرسال ملف عشوائي
            rl = random.randint(29, 31) 
            url = f"https://t.me/j8_ie/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
          
        elif call.data == "افراح":
            # إرسال ملف عشوائي
            rl = random.randint(50, 117) 
            url = f"https://t.me/sossosic/{rl}"
            bot.send_audio(
                call.message.chat.id,
                url,
                reply_to_message_id=call.message.message_id
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    except Exception as e:
        print(f"حدث خطأ: {e}")
        bot.send_message(call.message.chat.id, f"حدث خطأ أثناء إرسال الصوت: {e}")
        while True:
            try:
                print("Starting bot polling...")
                bot.polling()
            except Exception as e:
                print(f"Error occurred: {e}")
                print("Restarting bot polling...")
