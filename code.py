# from database import ApprovedUser, get_approved_users, remove_approved_user, add_approved_user
from telethon import TelegramClient, events, Button
import requests, os, operator, asyncio, random, time
from googletrans import Translator
from bs4 import BeautifulSoup
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
# @ABH.on(events.NewMessage(pattern='^سماح$'))
# async def approve_user(event):
#     if event.is_group and event.sender_id in admins:
#         if event.is_reply:
#             reply_message = await event.get_reply_message()
#             user_id = reply_message.sender_id
#             group_id = event.chat_id
#             user = reply_message.sender.first_name
#             add_approved_user(user_id, group_id)
#             await event.reply(f"تم السماح للمستخدم {user}بالتعديل الحر .")
#         else:
#             await event.reply("عزيزي المشرف الفاهي... \n يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
#     else:
#         return
# @ABH.on(events.NewMessage(pattern='^رفض$'))
# async def disapprove_user(event):
#     if event.is_group and event.sender_id in admins:
#         if event.is_reply:
#             reply_message = await event.get_reply_message()
#             user_id = reply_message.sender_id
#             group_id = event.chat_id
#             user = reply_message.sender.first_name
#             remove_approved_user(user_id, group_id)
#             await event.reply(f"المستخدم {user} تم رفض تعديلاتة القادمة \n والله خطية.")
#         else:
#             await event.reply("عزيزي المشرف الاغبر... \n يرجى الرد على رسالة المستخدم الذي تريد رفضه بالتعديلات.")
#     else:
#         return
# @ABH.on(events.NewMessage(pattern='^المسموح لهم$'))
# async def list_approved_users(event):
#     senid = event.sender_id
#     if event.is_group and senid in admins:
#         approved_users = get_approved_users(event.chat_id)
#         if approved_users:
#             approved_list = ""
#             for user_id, group_id in approved_users:
#                 try:
#                     user = await event.client.get_entity(user_id)
#                     user_name = user.username if user.username else user.first_name
#                     approved_list += f"{user_name} - {user_id} \n"
#                 except Exception as e:
#                     approved_list += f"خطأ في جلب اسم المستخدم: {user_id}\n"
#             await event.reply(f"📝 قائمة المستخدمين ال VIP بالتعديلات:\n{approved_list}")
#         else:
#             await event.reply("ماكو مستخدمين VIP او HIGH CLASS حالياً \n ضيفلك كم واحد حبيبي.") 
#     else:
#         return
# admins = [
#     1910015590,
#     7176263278,
#     6783332896,
#     1494932118,
#     201728276,
#     1688194818,
#     5399306464,
#     6498922948,
#     1446637898
# ]
# @ABH.on(events.MessageEdited)
# async def echo(event):
#     if event.is_group:
#         user_id = event.sender_id
#         group_id = event.chat_id
#         approved_users = get_approved_users(group_id)
#         approved_user_ids = [user[0] for user in approved_users]
#         if user_id in admins or user_id in approved_user_ids:
#             return
#         if event.media or ('http://' in event.message.message or 'https://' in event.message.message):
#             await event.reply("هنالك شخص عدل رسالة لكن غير معروف المقصد 🤔")
#         else:
#             return
#     else:
#         return
questions_and_answers = [
    {"question": "من هم ال البيت؟", "answer": "هم اهل بيت رسول الله"},
    {"question": "من هو الخليفة الاول؟", "answer": ["ابا الحسن علي", "الامام علي"]},
    {"question": "كم عدد المعصومين؟", "answer":14},
    {"question": "كم عدد اهل البيت؟", "answer":12},
    {"question": "من هو الذي دفن الامام علي؟", "answer": "شخص يشبه الامام علي"},
    {"question": "من هو الدنيئ الذي غدر الامام علي بالمسجد يوم 19 رمضان؟", "answer": "اللعين ابن ملجم"},
    {"question": "من الذي قال يا ابن راعية المعزة وعلئ من؟", "answer": "الامام الحسين , الشمر اللعين"},
    {"question": "الامام الذي بعد الامام علي؟", "answer": "الحسن المجتبى"},
    {"question": "الامام الذي بعد الامام الحسن؟", "answer": "الحسين الشهيد"},
    {"question": "بحق من نزلت اية التطهير؟", "answer": "ال بيت رسول الله"},
    {"question": "من هو سيف الله المسلول؟", "answer": "الامير علي"},
    {"question": "من هو سيف الشيطان المذلول؟", "answer": "خالد"},
    {"question": "من هم الثقلين؟", "answer": "كتاب الله واهل البيت"},
    {"question": "من هو قمر عشيرة الهواشم؟", "answer": "الامام العباس"},
    {"question": "من هو كفيل زينب؟", "answer": "الامام العباس"},
    {"question": "من الذي قتل المحسن ابن علي؟", "answer": "اللعين عمر"},
    {"question": "من هو قطيع الكفين؟", "answer": "الامام العباس"},
    {"question": "من هو شاعر قصيدة الله يا حامي الشريعة؟", "answer": "حيدر الحلي"},
    {"question": "من هو حامي الجار؟", "answer": "الامام علي"},
    {"question": "من صاحب قول \n أَمْلَأَ رُكابِي فِضَّةً أَوْ ذَهَبًا إِنِّي قَتَلْتُ خَيْرَ الرِّجَالِ أَمَّا وَأَبَا؟", "answer": "سنان بن انس"},
    {"question": "من هو سلمان المحمدي؟", "answer": "صحابي النبي و شهيد كربلاء"},
    {"question": "من هو الذي دفن مع الامام الحسين؟", "answer": "عبد الله الرضيع"},
    {"question": "ما هي اسم الواقعه في يوم العاشر من محرم؟", "answer": "واقعة الطف"},
    {"question": "ما هو اسم اليوم الذي استشهد فيه الامام الحسين؟", "answer": "عاشوراء"},
    {"question": "من هو الحجة المنتظر؟", "answer": "الامام المهدي"},
    {"question": "كم عدد المعصومين الذي اسمهم محمد؟", "answer": "2"},
    {"question": "ما هو اسم الامام المهدي؟", "answer": "محمد ابن الحسن"},
    {"question": "ما هي بيعة الغدير؟", "answer": "تتويج الامام علي"},
    {"question": "من هو الذي تصدق في المحبس في الصلاة؟", "answer": "الامام علي"},
    {"question": "ما هو اسم المكان الذي تم تتويج الامام علي خليفة؟", "answer": "غدير خم"},
    {"question": "اين دفنت ام البنين؟", "answer": "في البقيع"},
    {"question": "متى ولادة الامام المهدي \n عجل الله فرجة الشريف؟", "answer": " 15 من شعبان"},
    {"question": "من القائل , بين الحق والباطل 4 اصابع؟", "answer": "الامام علي"},
    {"question": "من هو الصادق الامين؟", "answer": "النبي محمد"},
    {"question": "من هو الرسول الاعظم؟", "answer": "الرسول محمد"},
    {"question": "من هو قائد الغر المحجلين؟", "answer": "الامام علي"},
    {"question": "من قائل مثلي لا يبايع مثله؟", "answer": "الامام الحسين"},
    {"question": "الان انكسر ظهري \n قالها الحسين لكن بحق من؟", "answer": "الامام العباس"},
    {"question": "من هو الفاروق الاعظم؟", "answer": "الامام علي"},
    {"question": "من هو سيد الشهداء؟", "answer": "الامام الحسين"},
    {"question": "من هو الذي اسقط عائشة في حرب الجمل؟", "answer": "الامام الحسن"},
    {"question": "ما انصفوكِ صانوا حرائرهم واخرجوكِ \n قالها الامام علي لكن بحق من؟", "answer": "عائشة"},
    {"question": "الخسف في البيداء هي علامة من علامات؟", "answer": "ظهور الامام"},
    {"question": "ما هو اسم خيل الامام الحسين؟", "answer": "الميمون"},
    {"question": "ما هو اشقئ الاولين والاخرين؟", "answer": "ابن ملجم"},
    {"question": "من هو مفرح قلب الزهراء؟", "answer": "ابو لؤلؤة"}
]
user_states = {}
@ABH.on(events.NewMessage(pattern='اسئلة|/quist'))
async def check_answer(event):
    user_id = event.sender_id
    user_message = event.text.strip().lower()

    if user_id in user_states and user_states[user_id].get("waiting_for_answer"):
        current_question = user_states[user_id].get("question", {})
        correct_answer = current_question.get('answer', '')

        if isinstance(correct_answer, str):
            correct_answer = correct_answer.lower()
        else:
            correct_answer = str(correct_answer)

        if user_message == correct_answer:
            await event.reply("أحسنت! إجابة صحيحة.")
            del user_states[user_id]
        else:
            await event.reply("إجابة خاطئة، حاول مرة أخرى.")
          
player1 = None
player2 = None
turn = None  
game_board = [" " for _ in range(9)] 
restart_confirmations = {}

@ABH.on(events.NewMessage(pattern='اكس او|/xo|/Xo'))
async def start_message(event):
    global player1, player2, username1, t1
    player1 = event.sender_id
    username1 = event.sender.username or "unknown"
    t1 = event.sender.first_name or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"start")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username1})! تم تسجيلك في لعبة x o انت الاعب الاول و دورك هو x.",
        file="https://t.me/VIPABH/1216",  
        parse_mode="Markdown",
        buttons=markup
    )

@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"start"))
async def start_game(event):
    global player1, player2, turn, game_board, username1, username2, t1, t2
    player2 = event.sender_id
    username2 = event.sender.username or "unknown"
    t2 = event.sender.first_name or "unknown"
    if player1 == player2:
        await event.answer(" لا يمكنك اللعب ضد نفسك يا متوحد!")
        return
    if player2 == 7017022402:
        return
    turn = player1
    game_board = [" " for _ in range(9)]
    await show_board(event)

async def show_board(event, winner=None):
    if winner:
        markup = [
            [Button.inline("إعادة اللعبة", b"restart"), Button.inline("إلغاء", b"cancel")]
        ]
        await event.edit(
            f"اللاعب [{winner['name']}](https://t.me/{winner['username']}) فاز باللعبة!",
            buttons=markup,
            parse_mode="Markdown"
        )
    elif " " not in game_board:
        markup = [
            [Button.inline("إعادة اللعبة", b"restart"), Button.inline("إلغاء", b"cancel")]
        ]
        await event.edit(
            "اللعبة انتهت بالتعادل!",
            buttons=markup,
            parse_mode="Markdown"
        )
    else:
        markup = [
            [Button.inline(game_board[0], b"move_0"), Button.inline(game_board[1], b"move_1"), Button.inline(game_board[2], b"move_2")],
            [Button.inline(game_board[3], b"move_3"), Button.inline(game_board[4], b"move_4"), Button.inline(game_board[5], b"move_5")],
            [Button.inline(game_board[6], b"move_6"), Button.inline(game_board[7], b"move_7"), Button.inline(game_board[8], b"move_8")]
        ]
        
        current_player = t1 if turn == player1 else t2
        current_username = username1 if turn == player1 else username2
        try:
            await event.edit(
                f"اللاعب الأول —> [{t1}](https://t.me/{username1})\nاللاعب الثاني —> [{t2}](https://t.me/{username2})\n\nدور اللاعب —> [{current_player}](https://t.me/{current_username})",
                buttons=markup,
                parse_mode="Markdown"
            )
        except Exception:
            await event.reply(
                f"اللاعب الأول —> [{t1}](https://t.me/{username1})\nاللاعب الثاني —> [{t2}](https://t.me/{username2})\n\nدور اللاعب —> [{current_player}](https://t.me/{current_username})",
                buttons=markup,
                parse_mode="Markdown"
            )

@ABH.on(events.CallbackQuery(func=lambda call: call.data.startswith(b"move_")))
async def make_move(event):
    global game_board, turn, t1, t2

    move = int(event.data.decode("utf-8").split("_")[1])
    
    if move < 0 or move >= len(game_board):
        await event.answer("التحرك غير صالح! اختر مربعاً آخر.")
        return

    if game_board[move] != " ":
        await event.answer("المربع هذا مشغول بالفعل! اختر مربعاً آخر.")
        return

    if event.sender_id == player1 and turn == player1:
        game_board[move] = "X"
        turn = player2  
    elif event.sender_id == player2 and turn == player2:
        game_board[move] = "O"
        turn = player1 
    else:
        await event.answer("ليس دورك الآن!")
        return

    winner = check_winner()
    if winner:
        winner_name = t1 if winner == "X" else t2
        winner_username = username1 if winner == "X" else username2
        await show_board(event, winner={"name": winner_name, "username": winner_username})
    elif " " not in game_board:
        await show_board(event)
    else:
        await show_board(event)

def check_winner():
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for line in lines:
        if game_board[line[0]] == game_board[line[1]] == game_board[line[2]] and game_board[line[0]] != " ":
            return game_board[line[0]]  
    return None

@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"restart"))
async def restart_game(event):
    global restart_confirmations, player1, player2, turn, game_board
    player_id = event.sender_id
    restart_confirmations[player_id] = True

    if player1 in restart_confirmations and player2 in restart_confirmations:
        game_board = [" " for _ in range(9)]
        turn = player1
        restart_confirmations = {}
        await show_board(event)
    else:
        await event.answer("في انتظار موافقة اللاعب الآخر لإعادة اللعبة.")

@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"cancel"))
async def cancel_game(event):
    await event.edit("تم إلغاء اللعبة.")

def reset_game():
    global game_board, player1, player2, turn
    game_board = [" " for _ in range(9)]  
    player1 = None
    player2 = None
    turn = None
if not any([player1, player2]): 
    reset_game()    
@ABH.on(events.NewMessage(pattern=r'^احس$'))
async def mem1(event):
        url = "https://files.catbox.moe/euqqqk.jpg"  
        await event.client.send_file(event.chat_id, url, reply_to=event.message.id)
operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}
@ABH.on(events.NewMessage(pattern=r'احسب (\d+)\s*([\+\-\*/÷])\s*(\d+)'))
async def calc(event):
    try:
        match = event.pattern_match 
        a = int(match.group(1))
        mark = match.group(2)
        b = int(match.group(3))
        if mark in operations:
            result = operations[mark](a, b)
            await event.respond(f"النتيجة `{result}`", reply_to=event.message.id)
        else:
            await event.respond("عملية غير مدعومة!", reply_to=event.message.id)
    except ZeroDivisionError:
        await event.respond("خطأ: لا يمكن القسمة على صفر!", reply_to=event.message.id)
abh = [
    "ها",
    "تفظل",
    "كول",
    "اسمعك",
    "شرايد",
    "خلصني",
    "https://t.me/VIPABH/1214",
    "https://t.me/VIPABH/1215"
]
@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def reply(event):
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)

@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
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
    detected_language = translator.detect(original_text)
    if detected_language.lang == "ar": 
        translated = translator.translate(original_text, dest="en")
    else: 
        translated = translator.translate(original_text, dest="ar")

    response = (
        f"اللغة المكتشفة: {detected_language.lang}\n"
        f"النص المترجم: `{translated.text}`"
    )
    await event.reply(response)

@ABH.on(events.NewMessage(pattern='ابن هاشم'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        rl = random.randint(242, 255)
        url = f"https://t.me/iuABH/{rl}"  
        caption = "ابن هاشم (رض) مرات متواضع ،🌚 @K_4x1" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='زهراء'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://t.me/VIPABH/1220"  
        caption = "@klix_78 ( لَقَدْ كَفَرَ الّذِينَ قَالُوا إنَّ الله هُو المَسِيحُ ابْنُ مَرْيَم)." 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='امريجا|الامريكي'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://files.catbox.moe/p9e75j.mp4"  
        caption = "@l_h_2" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='امير'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://files.catbox.moe/k44qq6.mp4"  
        caption = "@xcxx1x" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
@ABH.on(events.NewMessage(pattern='عبدالله|عبود'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://files.catbox.moe/qohqtp.MP4"  
        caption = "@UU77QQ" 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return
auto = [
        "ع س",
        "عليكم السلام",
        "عليكم السلام والرحمة والاكرام",
        "عليكم سلام الله"
        ]
@ABH.on(events.NewMessage(pattern=r'^(سلام عليكم|السلام عليكم)$'))
async def reply_abh(event):
        abh = random.choice(auto)
        await event.reply(abh)    

@ABH.on(events.NewMessage(pattern=r'^(مخفي طكة زيج|زيج)$'))
async def reply_abh(event):
    replied_message = await event.get_reply_message()
    if replied_message:
        await event.client.send_file(replied_message.peer_id, "https://t.me/VIPABH/1171", reply_to=replied_message.id)
    else:
        await event.reply("يجب عليك الرد على رسالة حتى يعمل هذا الأمر.")


url = "https://ar.wikipedia.org/w/api.php"
searching_state = {}
@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عن')))
async def cut(event):
    search_term = event.text.strip().lower().replace('ابحث عن', '').strip()

    if not search_term:
        await event.reply("من فضلك أدخل الكلمة التي تريد البحث عنها بعد 'ابحث عن'.")
        return
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "utf8": 1,
        "srlimit": 3  
    }
    response = requests.get(url, params=params)   
    if response.status_code == 200:
        data = response.json()
        if 'query' in data and 'search' in data['query']:
            if not data['query']['search']:
                await event.reply("لا يوجد نتائج لهذا البحث.")
            else:
                found_exact_match = False
                for result in data['query']['search']:
                    if result['title'].lower() == search_term:
                        found_exact_match = True
                        snippet = BeautifulSoup(result['snippet'], "html.parser").get_text()
                        snippet = snippet[:1000] + "..." if len(snippet) > 1000 else snippet  # 1000 حرف هنا
                        article_url = f"https://ar.wikipedia.org/wiki/{result['title']}"
                        
                        await event.reply(f"عنوان المقال: \n {result['title']}\n"
                                          f"المقال: \n {snippet}\n"
                                          f"{'-' * 40}")
                
                if not found_exact_match:
                    await event.reply(
                        f"لا يوجد نتائج تطابق {search_term} \n لكن جرب `ابحث عام {search_term}`",
                        parse_mode="Markdown"
                                     )                    
        else:
            await event.reply("حدث خطأ في استجابة API.")
    else:
        await event.reply(f"حدث خطأ في الاتصال بـ Wikipedia. حاول مرة أخرى لاحقًا.")

searching_state = {}
@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower().startswith('ابحث عام')))
async def start_search(event):
    searching_state[event.chat.id] = True
    search_term = event.text.strip().lower().replace('ابحث عام', '').strip()
    if not search_term:
        await event.reply("من فضلك أدخل الكلمة التي تريد البحث عنها بعد 'ابحث عام'.")
        return
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "utf8": 1,
        "srlimit": 3  
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'query' in data and 'search' in data['query']:
            if not data['query']['search']:
                await event.reply("لم يتم العثور على نتائج لهذا البحث.")
            else:
                for result in data['query']['search']:
                    snippet = BeautifulSoup(result['snippet'], "html.parser").get_text()
                    snippet = snippet[:400] + "..." if len(snippet) > 400 else snippet  # 400 حرف هنا
                    article_url = f"https://ar.wikipedia.org/wiki/{result['title']}"
                    
                    await event.reply(f"عنوان المقال: \n {result['title']}\n"
                                      f"المقال: \n {snippet}\n"
                                      f"{'-' * 40}")
        else:
            await event.reply("حدث خطأ في استجابة API.")
    else:
        await event.reply(f"حدث خطأ: {response.status_code}")
    searching_state[event.chat.id] = False

@ABH.on(events.NewMessage(func=lambda e: e.text and e.text.strip().lower() in ['عاشوراء']))
async def ashouau(event):
    pic = "links/abh.jpg"
    await ABH.send_file(event.chat_id, pic, caption="تقبل الله صالح الأعمال", reply_to=event.message.id)

group_game_status = {}
number2 = None
game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
points = {}

def format_board(game_board, numbers_board):
    """تنسيق الجدول للعرض بشكل مناسب"""
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board

def reset_game(chat_id):
    """إعادة تعيين حالة اللعبة بعد انتهائها"""
    global game_board, number2, group_game_status
    game_board = [row[:] for row in original_game_board]
    number2 = None
    group_game_status[chat_id]['game_active'] = False
    group_game_status[chat_id]['active_player_id'] = None

group_game_status = {}

@ABH.on(events.NewMessage(pattern='/rings'))
async def start_game(event):
    username = event.sender.username or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"startGame")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1210",  
        parse_mode="Markdown",
        buttons=markup
    )
    
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"startGame"))
async def handle_start_game(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    username = event.sender.username or "unknown"
    
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'game_active': False, 'active_player_id': None}    
    if not group_game_status[chat_id]['game_active']:
        group_game_status[chat_id]['game_active'] = True
        group_game_status[chat_id]['active_player_id'] = user_id
    
        global number2
        number2 = random.randint(1, 6)
        group_game_status[chat_id]['number2'] = number2
        await event.edit(buttons=None)
        await event.respond(
            f"عزيزي [{event.sender.first_name}](https://t.me/@{username})! تم تسجيلك في لعبة محيبس \nارسل `جيب ` + رقم للحزر \n ارسل `طك ` + رقم للتخمين.",
            parse_mode="Markdown"
        )

@ABH.on(events.NewMessage(pattern=r'جيب (\d+)'))
async def handle_guess(event):
    global number2, game_board, points, group_game_status
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        try:
            guess = int(event.text.split()[1])  
            if 1 <= guess <= 6:  
                if guess == number2:
                    winner_id = event.sender_id 
                    points[winner_id] = points.get(winner_id, 0) + 1 
                    sender_first_name = event.sender.first_name
                    game_board = [["💍" if i == number2 - 1 else "🖐️" for i in range(6)]]
                    await event.reply(f'🎉 الف مبروك! اللاعب ({sender_first_name}) وجد المحبس 💍!\n{format_board(game_board, numbers_board)}')
                    reset_game(chat_id)
                else:
                    sender_first_name = event.sender.first_name
                    game_board = [["❌" if i == guess - 1 else "🖐️" for i in range(6)]]
                    await event.reply(f"ضاع البات ماضن بعد تلگونة ☹️ \n{format_board(game_board, numbers_board)}")
                    reset_game(chat_id)
            else:
                await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")  # إذا كان الرقم خارج النطاق
        except (IndexError, ValueError):
            await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")  # إذا كانت المدخلات غير صحيحة

@ABH.on(events.NewMessage(pattern=r'طك (\d+)'))
async def handle_strike(event):
    global game_board, number2, group_game_status
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        try:
            strike_position = int(event.text.split()[1])  
            if strike_position == number2:
                game_board = [["💍" if i == number2 - 1 else "🖐️" for i in range(6)]]
                await event.reply(f"**خسرت!** \n{format_board(game_board, numbers_board)}")
                reset_game(chat_id)
            else:
                abh = [
                    "تلعب وخوش تلعب 👏🏻",
                    "لك عاش يابطل استمر 💪🏻",
                    "على كيفك ركزززز انتَ كدها 🤨",
                    "لك وعلي ذيييب 😍"
                ]
                iuABH = random.choice(abh)
                game_board[0][strike_position - 1] = '🖐️'
                await event.reply(f" {iuABH} \n{format_board(game_board, numbers_board)}")
        except (IndexError, ValueError):
            await event.reply("❗ يرجى إدخال رقم صحيح بين 1 و 6.")
            
@ABH.on(events.NewMessage(pattern='/محيبس'))
async def show_number(event):
    """إظهار الرقم السري عند الطلب وإرساله إلى @k_4x1"""
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        target_user_id = 1910015590  
        await ABH.send_message(target_user_id, f"الرقم السري هو: {number2}")
        await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
    else:
        await event.reply("لم تبدأ اللعبة بعد. أرسل /rings لبدء اللعبة.")

mohmurl = random.randint(119, 138)
basimurl = random.randint(50, 118)
musurl = random.randint(139, 154)
nurl = random.randint(164, 170)
furl = random.randint(171, 174)

async def send_audio_from_list(call, url_list):
    rl = random.choice(url_list)
    audio_url = f"https://t.me/sossosic/{rl}"
    await call.respond(
        file=audio_url
    )
    
@ABH.on(events.NewMessage(func=lambda event: event.text in ['لطمية', 'لطميه']))

async def start(event):
    username = event.sender.username or "لا يوجد اسم مستخدم"
    markup = [
        [Button.inline("إرسال لطمية عشوائية", b"send_latmia")]
    ]

    await event.respond(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username}) حياك الله! اضغط على الزر أدناه للحصول على لطمية عشوائية.",
        file="https://t.me/VIPABH/1212",
        buttons=markup,
        parse_mode="md"
    )
banned_url = [
    9,  25, 94, 131, 175,
    26, 40, 110, 136, 194,
    71, 72, 111, 142, 212,
    77, 79, 114, 148,
    80, 81, 115, 150,
    82, 93, 121, 152
    ]
latmiyat_range = range(50, 226) 
async def send_random_latmia(call):
    try:
        chosen = random.choice(latmiyat_range)
        if chosen in banned_url:
            return await send_random_latmia(call)
        latmia_url = f"https://t.me/x04ou/{chosen}"
        await call.reply(file=latmia_url)
    except Exception as e:
        await call.reply(f"حدث خطأ أثناء الإرسال: {str(e)}")

@ABH.on(events.CallbackQuery)
async def handle_callback(call):
    if call.data == b"send_latmia":  
        await send_random_latmia(call)
        await call.edit(buttons=None) 
    else:
        return
@ABH.on(events.NewMessage(pattern='/start'))
async def handle_start(event):
    await event.reply(
        "أهلاً حياك الله! \n\n"
        "• أرسل /xo ل بدء لعبة xo \n"
        "• أرسل `لطمية` ل ارسال لطمية\n"
        "• أرسل /num لبدء لعبة الأرقام.\n"
        "• أرسل `ميم` او `ميمز` للميمز. \n"
        "• أرسل `كتويت` لبدء أسئلة الكتتويت.\n"
        "• أرسل /quist او `اسئلة`اسئلة دينية. \n"
        "• أرسل `ابحث عن` لعمل بحث في ويكيبيديا \n"
        "• أرسل /rings لبدء لعبة محيبس الكتتويت. \n"
        "• أرسل `النقاط` ل رؤية نقاطك في لعبة /num \n"
        "• الامر او بالرد `ترجمة` لترجمه نص مع لطمية\n"
        "• أرسل `احسب` لحساب معادلة بالرد او مع الامر\n"
        "• أرسل `ابحث عام` يعمل بحث لكن ليس دقيق ب 3 نتائج \n\n"
        "استمتع! 🎉",
        parse_mode='markdown'
        )
        
def add_or_update_user(user_id):
    if user_id not in user_points:
        user_points[user_id] = 0  
            
def add_point_to_winner(user_id):
    if user_id in user_points:
        user_points[user_id] += 1 

def get_user_score(user_id):
    return user_points.get(user_id, 0)

user_points = {}
game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None
@ABH.on(events.NewMessage(pattern='/num'))
async def start_game(event):
    global game_active, number, attempts, active_player_id

    if game_active:
        await event.reply("اللعبة قيد التشغيل بالفعل! حاول إنهاء اللعبة الحالية أولاً.")
        return
    username = event.sender.username if event.sender.username else "لا يوجد اسم مستخدم"
    markup = [[Button.inline("ابدأ اللعبة", b"start_game")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1204",
        parse_mode="Markdown",
        buttons=markup
    )

@ABH.on(events.CallbackQuery(data=b"start_game"))
async def initiate_game(event):
    global game_active, number, attempts, active_player_id

    game_active = True
    number = random.randint(1, 10)
    attempts = 0
    active_player_id = event.sender_id

    await event.answer("🎮 اللعبة بدأت!")
    await event.edit("🎲 اللعبة بدأت! حاول تخمين الرقم (من 1 إلى 10).")
@ABH.on(events.NewMessage(func=lambda event: game_active and event.sender_id == active_player_id))
async def handle_guess(event):
    global game_active, number, attempts, max_attempts

    if not game_active:
        await event.reply("اللعبة ليست نشطة حاليًا، ابدأ لعبة جديدة.")
        return

    try:
        guess = int(event.text)
    except ValueError:
        await event.reply("يرجى إدخال رقم صحيح بين 1 و 10.")
        return

    if guess < 1 or guess > 10:
        await event.reply("يرجى اختيار رقم بين 1 و 10 فقط!")
        return

    attempts += 1

    if guess == number:
        add_or_update_user(event.sender_id)
        add_point_to_winner(event.sender_id)
        points = get_user_score(event.sender_id)

        msg1 = await event.reply("🥳")
        await asyncio.sleep(3)
        await msg1.edit("🎉مُبارك! لقد فزت!")
        game_active = False
    elif attempts >= max_attempts:
        await event.reply(f"للأسف، لقد نفدت محاولاتك. الرقم الصحيح هو {number}.")
        lose = "https://t.me/VIPABH/23"
        await ABH.send_message(event.chat_id, file=lose)
        game_active = False
    else:
        await event.reply("جرب مرة أخرى، الرقم غلط💔")

@ABH.on(events.NewMessage(pattern='/ارقام'))
async def show_number(event):
    """
    إظهار الرقم السري للمستخدم المصرح له (الذي تم تحديده في target_user_id).
    """
    global game_active, number
    chat_id = event.chat_id
    target_user_id = 1910015590 
    if game_active:
        # try:
            ms1 = await ABH.send_message(target_user_id, f"🔒 الرقم السري هو: {number}")
            await event.reply("تم إرسال الرقم السري إلى @k_4x1.")

            await asyncio.sleep(10)
            await ABH.delete_messages(ms1.chat_id, [ms1.id])  
        # except Exception as e:
        #     await event.reply(f"حدث خطأ: {str(e)}")
    else:
        await event.reply("⚠️ لم تبدأ اللعبة بعد. أرسل /num لبدء اللعبة.")

@ABH.on(events.NewMessage(pattern='النقاط')) 
async def show_points(event):
    user_id = event.sender_id  
    points = get_user_score(user_id) 
    await event.reply(f"📊 نقاطك الحالية هي: {points} 🌟")


questions = [
    "شلون تعمل هالشي؟",
    "شلون تقضي وقتك بالفراغ؟",
    "شلون تتحكم بالضغط؟",
    "شلون تكون صبور؟",
    "شلون تحافظ على التركيز؟",
    "شلون تكون قوي نفسياً؟",
    "شلون تسيطر على الغضب؟",
    "شلون تدير وقتك بشكل فعال؟",
    "شلون تكون ناجح في حياتك المهنية؟",
    "شلون تطور مهاراتك الشخصية؟",
    "شلون تدير الضغوطات في العمل؟",
    "شلون تدير الامور المالية؟",
    "شلون تتعلم لغة جديدة؟",
    "شلون تكون مبدع في عملك؟",
    "شلون تطور علاقاتك الاجتماعية؟",
    "شلون تتغلب على التحديات؟",
    "شلون تنظم حياتك بشكل منظم؟",
    "شلون تحافظ على صحتك؟",
    "شلون تحمي نفسك من الإجهاد؟",
    "شلون تعتني بنفسك بشكل جيد؟",
    "شلون تكون متفائل في الحياة؟",
    "شلون تدير الوقت بين العمل والحياة الشخصية؟",
    "شلون تتعامل مع الشكوك والتوتر؟",
    "شلون تعطي قيمة لوقتك؟",
    "شلون تدير التوتر في العلاقات العائلية؟",
    "شلون تتعلم من الاخطاء؟",
    "شلون تدير الصعوبات في الحياة؟",
    "شلون تكون منظم في حياتك اليومية؟",
    "شلون تحسن من تركيزك وانتباهك؟",
    "شلون تطور مهاراتك الشخصية والاجتماعية؟",
    "شلون تدير العمل في فريق؟",
    "شلون تحسن من قدراتك التواصلية؟",
    "شلون تكون منظم في الدراسة؟",
    "شلون تكون فعال في استخدام التكنولوجيا؟",
    "شلون تحافظ على توازنك بين العمل والحياة الشخصية؟",
    "شلون تتعلم مهارات جديدة بسرعة؟",
    "شلون تكون ملهماً للآخرين؟",
    "شلون تدير الخلافات في العمل؟",
    "شلون تكون مؤثراً في العروض التقديمية؟",
    "شلون تحسن من قدراتك التفكير الإبداعي؟",
    "شلون تطور قدراتك القيادية؟",
    "شلون تكون متفائل في ظروف صعبة؟",
    "شلون تدير التحولات في الحياة؟",
    "شلون تتعلم من النجاحات والإخفاقات؟",
    "شلون تكون مستعداً للتغيير؟",
    "شلون تستمتع بالحياة؟",
    "شلون تكون إنساناً محبوباً ومحترماً؟",
    "شلون تتعلم من خبرات الآخرين؟",
    "شلون تطور مهاراتك في التعلم الذاتي؟",
    "شلون تحسن من قدراتك على اتخاذ القرارات؟",
    "شلون تكون مبادراً في العمل؟",
    "شلون تطور مهاراتك في حل المشكلات؟",
    "شلون تستفيد من النقد البناء؟",
    "شلون تطور ثقتك بالنفس؟",
    "شلون تتعامل مع التغييرات في العمل؟",
    "شلون تطور مهاراتك في التعاون والعمل الجماعي؟",
    "شلون تتعامل مع الضغوطات في الحياة؟",
    "شلونك؟",
    "شنو اسمك؟",
    "شنو جنسيتك؟",
    "شنو عمرك؟",
    "شنو لونك المفضل؟",
    "شنو طبخة تحبها اكثر؟",
    "شنو هوايتك المفضلة؟",
    "شنو مكان سفرة اللي تحلم تروحله؟",
    "شنو نوع السيارة اللي تفضلها؟",
    "شنو نوع الموسيقى اللي تحب تستمع لها؟",
    "شنو تحب تسوي في وقت الفراغ؟",
    "شنو اكلتك المفضلة في الفطور؟",
    "شنو اكلتك المفضلة في الغدا؟",
    "شنو اكلتك المفضلة في العشا؟",
    "شنو نوع الشاي اللي تحب تشربه؟",
    "شنو نوع القهوة اللي تحب تشربها؟",
    "شنو اكثر شيء مميز في ثقافة العراق؟",
    "شنو نوع الافلام اللي تحب تشوفها؟",
    "شنو البلدة العربية اللي تفضل تزورها؟",
    "شنو نوع الهدية اللي تحب تتلقاها؟",
    "شنو اهم شيء بالنسبة إليك في الصداقة؟",
    "شنو الشيء اللي تشوفه عند العراقيين بشكل خاص؟",
    "شنو الاكلة العراقية المفضلة عندك؟",
    "شنو نوع الرياضة اللي تحب تمارسها؟",
    "شنو مكان العراقي اللي تحب تزوره في العراق؟",
    "شنو اكثر شيء تحبه في الطبيعة؟",
    "شنو اللون اللي يحبه العراقيين كثير؟",
    "شنو الشيء اللي يستفزك بسرعة؟",
    "شنو الشيء اللي يخليك تفرح؟",
    "شنو الشيء اللي تحس إنه اكثر شيء يعبر عن الهوية العراقية؟",
    "شنو نوع الهاتف اللي تستخدمه؟",
    "شنو الشيء اللي تحس فيه إنه مفقود في المجتمع العراقي؟",
    "شنو اكثر مكان تحب تزوره في العراق؟",
    "شنو النصيحة اللي تحب تعطيها لشخص صغير؟",
    "شنو الشيء اللي يخليك تشعر بالراحة والهدوء؟",
    "شنو الشيء اللي تحب تسويه بالعطلة؟",
    "شنو الحيوان اللي تحبه اكثر؟",
    "شنو الشيء اللي تحب تهديه لشخص عزيز عليك؟",
    "شنو الشيء اللي تحس بإنجاز كبير إذا قمت به؟",
    "شنو اكثر موقع التواصل الاجتماعي اللي تستخدمه؟",
    "شنو الشيء اللي يحبه العراقيين في الاعياد والمناسبات؟",
    "شنو الشيء اللي تحب تشوفه في العراق مطور ومتطور؟",
    "شنو الشيء اللي تحب تشاركه مع الآخرين بشكل كبير؟",
    "شنو اكثر موسم تحبه في العراق؟",
    "شنو الشيء اللي تتمنى تغيره في العراق؟",
    "شنو الشيء اللي تحب تستثمر فيه وقتك وجهدك؟",
    "شنو الشيء اللي يميز العراق والعراقيين برايك؟",
    "شنو نوع الفن اللي تحب تستمتع به؟",
    "شنو الشيء اللي تحب تتعلمه في المستقبل؟",
    "شنو اكثر شيء تحبه في الشتاء؟",
    "شنو الشيء اللي يرفع معنوياتك بشكل سريع؟",
    "شنو الشيء اللي تحب تهديه لنفسك؟",
    "شنو الشيء اللي تتمنى تحققه في حياتك؟",
     "منو افضل صديق عندك؟",
    "منو شخصيتك المفضلة في الافلام؟",
    "منو الشخص اللي تحب تسافر معه؟",
    "منو الشخص اللي بتستشيره في قراراتك؟",
    "منو اكثر شخص تحب تشوفه كل يوم؟",
    "منو اكثر شخص غريب بتعرفه؟",
    "منو الشخص اللي تحب تحجي معه لساعات؟",
    "منو اكثر شخص قدوة بحياتك؟",
    "منو الشخص اللي تثق فيه بشكل كامل؟",
    "منو اكثر شخص ملهم في حياتك؟",
    "منو الشخص اللي تتمنى تشوفه اليوم؟",
    "منو الشخص اللي تحب تكون جارك؟",
    "منو الشخص اللي بتتحدث معه كل يوم؟",
    "منو الشخص اللي بتشتاقله كثير؟",
    "منو الشخص اللي بتعتمد عليه في الصعوبات؟",
    "منو الشخص اللي تحب تشاركه اسرارك؟",
    "منو الشخص اللي بتقدر قيمته في حياتك؟",
    "منو الشخص اللي تحب تطلب منه المشورة؟",
    "منو الشخص اللي تحب تكون معه في المشاكل؟",
    "منو الشخص اللي بتحسه اكثر شخص يفهمك؟",
    "منو الشخص اللي تحب تحتفل معه في الاعياد؟",
    "منو الشخص اللي تتوقعه اكثر شخص بيرحل عنك؟",
    "منو الشخص اللي تحب تشترك معه في الهوايات؟",
    "منو الشخص اللي تحب تشوفه بعد غياب طويل؟",
    "منو الشخص اللي تتمنى تقدمله هدية مميزة؟",
    "منو الشخص اللي تحب تذهب معه في رحلة استكشافية؟",
    "منو الشخص اللي تحب تحجي معه عن مشاكلك العاطفية؟",
    "منو الشخص اللي تتمنى تكون له نفس قدراتك ومهاراتك؟",
    "منو الشخص اللي تحب تقابله وتشتغل معه في المستقبل؟",
    "منو الشخص اللي تحب تحتفل معه بنجاحك وإنجازاتك؟",
    "منو الشخص اللي بتتذكره بكل سعادة عندما تراجع صورك القديمة؟",
    "منو الشخص اللي تحب تشاركه تجاربك ومغامراتك في الحياة؟",
    "منو الشخص اللي تحب تسمع نصائحه وتطبقها في حياتك؟",
    "منو الشخص اللي تحب تشوفه ضحكته بين الفينة والاخرى؟",
    "منو الشخص اللي تعتبره اكثر شخص يدعمك ويحفزك على تحقيق اهدافك؟",
    "منو الشخص اللي تحب تشوفه محقق نجاحاته ومستقبله المشرق؟",
    "منو الشخص اللي تحب تشكره على وجوده في حياتك ودعمه المستمر؟",
    "منو الشخص اللي تحب تقدمله هدية تذكارية لتخليك تذكره للابد؟",
    "منو الشخص اللي تحب تشكره على دعمه الكبير لك في مشوارك الدراسي؟",
    "منو الشخص اللي تتمنى تعرفه في المستقبل وتصير صداقتكم مميزة؟",
    "منو الشخص اللي تحب تشاركه لحظات الفرح والسعادة في حياتك؟",
    "منو الشخص اللي تعتبره اكثر شخص يستحق منك كل الحب والاحترام؟",
    "منو الشخص اللي تحب تشاركه اسرارك وتحجي له كل شيء بدون تردد؟",
    "منو الشخص اللي تتمنى تحضر معه حفلة موسيقية لفرقتك المفضلة؟",
    "منو الشخص اللي تحب تتنافس معه في لعبة او رياضة تحبها؟",
    "منو الشخص اللي تحب تشوفه مبتسماً ومتفائلاً في الحياة؟",
    "شوكت تفتح المحل؟",
    "شوكت بتروح على العمل؟",
    "شوكت تكون مستعد للمقابلة؟",
    "شوكت بتنوم بالليل؟",
    "شوكت بتصحى بالصبح؟",
    "شوكت بتسافر؟",
    "شوكت بتعود من العمل؟",
    "شوكت بتعمل رياضة؟",
    "شوكت بتذاكر للامتحان؟",
    "شوكت بتنظف البيت؟",
    "شوكت بتقرا الكتاب؟",
    "شوكت تكون فاضي للتسوق؟",
    "شوكت بتنطر الباص؟",
    "شوكت بتعود من السفر؟",
    "شوكت بتشتري الهدية؟",
    "شوكت بتتقابل مع صديقك؟",
    "شوكت بتحضر الحفلة؟",
    "شوكت بتتعشى؟",
    "شوكت بتتناول الفطور؟",
    "شوكت بتسافر في العطلة؟",
    "شوكت بترجع للمنزل؟",
    "شوكت تخلص المشروع؟",
    "شوكت بتتخرج من الجامعة؟",
    "شوكت بتبدا العمل؟",
    "شوكت بتفتح المحل؟",
    "شوكت تنتهي الدورة التدريبية؟",
    "شوكت بتتزوج؟",
    "شوكت بترتب الغرفة؟",
    "شوكت تتعلم الموسيقى؟",
    "شوكت بترتب الوثائق؟",
    "شوكت بتسجل في النادي الرياضي؟",
    "شوكت تستلم الطلبية؟",
    "شوكت بتشوف الطبيب؟",
    "شوكت بتتناول الغداء؟",
    "شوكت تكون مستعد للسفر؟",
    "شوكت بتكمل المشروع؟",
    "شوكت تخلص الواجب؟",
    "شوكت تحصل على النتيجة؟",
    "شوكت تتعلم اللغة الجديدة؟",
    "شوكت بتحضر المؤتمر؟",
    "شوكت بتنهي الكتاب؟",
    "شوكت بتفتح المطعم؟",
    "شوكت بتسافر في الإجازة؟",
    "شوكت بتبدا التدريب؟",
    "شوكت تخلص المشروع الفني؟",
    "شوكت تنتهي الجلسة؟",
    "شوكت تتعلم الطبخ؟",
    "شوكت تستلم الشهادة؟",
    "شوكت بتبدا الرحلة؟",
    "شوكت بتنهي الاعمال المنزلية؟",
    "شوكت تكون فاضي للقراءة؟",
    "شوكت تستلم السيارة الجديدة؟",
    "شوكت بتتناول العشاء؟",
    "وين رايح؟",
    "وين تسكن؟",
    "وين بتشتغل؟",
    "وين بتروح في ايام العطلة؟",
    "وين تحب تسافر في العطلات؟",
    "وين تحب تروح مع الاصدقاء؟",
    "وين تكون في الساعة الثامنة صباحاً؟",
    "وين تكون في الساعة العاشرة مساءً؟",
    "وين تحب تتناول الإفطار؟",
    "وين تحب تتسوق؟",
    "وين تحب تتناول العشاء؟",
    "وين تكون في الساعة الثانية ظهراً؟",
    "وين تحب تمضي امسياتك؟",
    "وين تحب تقضي ايام العطلة؟",
    "وين تحب تزور المعالم السياحية؟",
    "وين تحب تشتري الهدايا؟",
    "وين تحب تتمرن وتمارس الرياضة؟",
    "وين تحب تذهب للتسوق؟",
    "وين تحب تقضي وقتك مع العائلة؟",
    "وين تكون في الساعة الخامسة مساءً؟"
]
@ABH.on(events.NewMessage(func=lambda event: event.text in ['كتويت']))
async def send_random_question(event):
    random_question = random.choice(questions)
    await event.reply(random_question)

ABH.run_until_disconnected() 
