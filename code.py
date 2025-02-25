from telethon import TelegramClient, events, Button
import random, os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
choices = {"rock": "🪨حجره", "paper": "📜ورقة", "cuter": "✂️مقص"}
active_games = {}  
@ABH.on(events.NewMessage(pattern="حجرة|/rock"))
async def start(event):
 active_games[event.chat_id] = event.sender_id  
 buttons = [[Button.inline("🪨", b"rock"), Button.inline("✂️", b"cuter"), Button.inline("📜", b"paper")]]
 await event.respond("اختر أحد الاختيارات 🌚", buttons=buttons)
@ABH.on(events.CallbackQuery())
async def callback_handler(event):
 game_owner = active_games.get(event.chat_id)  
 if game_owner != event.sender_id:
  await event.answer("من تدخل في ما لا يعنيه لقي كلام لا يرضيه 🙄", alert=True)
  return  
 user_choice = event.data.decode("utf-8")
 if user_choice not in choices:
  return  
 bot_choice_key = random.choice(list(choices.keys()))
 bot_choice = choices[bot_choice_key]  
 user_id = event.sender_id
 result = "🤝تعادل" if user_choice == bot_choice_key else "🎉فزت" if (user_choice == "rock" and bot_choice_key == "cuter") or (user_choice == "paper" and bot_choice_key == "rock") or (user_choice == "cuter" and bot_choice_key == "paper") else "😢خسرت"
 await event.edit(f"📌اختيارك: [اضغط هنا](tg://user?id={user_id}) {choices[user_choice]}\n🤖مخفي: [اضغط هنا](tg://user?id=7908156943) {bot_choice}\n\n{result}")
ABH.run_until_disconnected()
