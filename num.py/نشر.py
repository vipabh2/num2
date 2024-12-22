from pyrogram import Client, filters
import time

@Client.on_message(filters.user(1910015590) & filters.command("نشر"))
def send_to_all_groups(client, message):
    message_text = " ".join(message.command[1:])
    
    for chat in client.iter_dialogs():
        if chat.chat.type == "group":
            try:
                client.send_message(chat.chat.id, text=message_text)
                print(f"تم إرسال الرسالة إلى المجموعة: {chat.chat.title}")
                time.sleep(1) 
            except Exception as e:
                print(f"حدث خطأ أثناء إرسال الرسالة إلى {chat.chat.title}: {e}")
