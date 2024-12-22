import telebot
import random
import time
import os


bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)
        
@bot.message_handler(func=lambda message: message.text in ['ميم'] or message.text in ['ميمز'])
def send_random_file(message):
    time.sleep(2)
    rl = random.randint(2, 255)
    url = f"t.me/iuabh/{rl}"
    if url == "t.me/iuabh/242":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/243":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/244":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/245":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/246":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/247":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/248":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/249":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/250":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/251":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/252":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/253":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/254":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    if url == "t.me/iuabh/255":
        bot.send_video(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
    else:
        # bot.send_photo(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)
        sent_message = bot.send_photo(message.chat.id, url, caption="😎يسعد مسائك", reply_to_message_id=message.message_id)

if __name__ == "__main__":
    bot.polling(none_stop=True)
