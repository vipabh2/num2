from Resources import football, questions, mention #type: ignore
from top import points, add_points #type: ignore
import random, asyncio, time, os, json
from telethon import Button, events
from ABH import ABH #type: ignore
from faker import Faker
@ABH.on(events.NewMessage(pattern=r'^شراء حل \s+([^\d\W]\w*)'))
async def buy(event):
    user_id = event.sender_id
    type = event.pattern_match.group(1)
    x = {'/football', 'كرة قدم', '/quist', '/sport', '/rings', '/num'}
    if type not in x:
        await event.reply('ماكو هيج لعبة')
    elif type == '/football':
        await event.reply(user_state[user_id]['answer'])
USER_DATA_FILE = "boxing.json"
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern=r'مضاربة (\d+)'))
async def boxing(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply('عزيزي، لازم ترد على رسالة الشخص اللي تريد تضاربه.')
        return
    try:
        count = int(event.pattern_match.group(1))
    except ValueError:
        await event.reply('تأكد من كتابة رقم صحيح بعد كلمة مضاربة.')
        return
    if count <= 2999:
        await event.reply('المبلغ يجب أن يكون أكبر من 3000.')
        return
    user1_id = reply.sender_id
    user2_id = event.sender_id
    gid = str(event.chat_id)
    user_data = load_user_data()
    current_time = int(time.time())
    last_target_time = user_data.get(str(user1_id), {}).get("boxed", 0)
    if current_time - last_target_time < 10 * 60:
        remaining = 10 * 60 - (current_time - last_target_time)
        minutes = remaining // 60
        seconds = remaining % 60
        s = await event.get_sender(event, s)
        x = await mention(event)
        await event.reply(f"لا يمكن مضاربة {x} الآن، انتظر {minutes:02}:{seconds:02} دقيقة.")
        return
    last_attack_time = user_data.get(str(user2_id), {}).get("attacked", 0)
    if current_time - last_attack_time < 10 * 60:
        remaining = 10 * 60 - (current_time - last_attack_time)
        minutes = remaining // 60
        seconds = remaining % 60
        await event.reply(f"يجب عليك الانتظار {minutes:02}:{seconds:02} قبل أن تبدأ مضاربة جديدة.")
        return
    if str(user1_id) not in points or gid not in points[str(user1_id)]:
        await event.reply('الشخص الذي تم الرد عليه لا يملك نقاط.')
        return
    if str(user2_id) not in points or gid not in points[str(user2_id)]:
        await event.reply('أنت لا تملك نقاط.')
        return
    mu1 = points[str(user1_id)][gid]['points']
    mu2 = points[str(user2_id)][gid]['points']
    if count > mu1:
        await event.reply('فلوس الشخص الذي تم الرد عليه أقل من مبلغ المضاربة.')
        return
    if count > mu2:
        await event.reply('فلوسك أقل من مبلغ المضاربة.')
        return
    user1_entity = await ABH.get_entity(user1_id)
    user2_entity = await ABH.get_entity(user2_id)
    mention1 = f"[{user1_entity.first_name}](tg://user?id={user1_id})"
    mention2 = f"[{user2_entity.first_name}](tg://user?id={user2_id})"
    winner_id = random.choice([user1_id, user2_id])
    loser_id = user2_id if winner_id == user1_id else user1_id
    points[str(winner_id)][gid]['points'] += count
    points[str(loser_id)][gid]['points'] -= count
    with open("points.json", "w", encoding="utf-8") as f:
        json.dump(points, f, ensure_ascii=False, indent=2)
    winner_name = mention1 if winner_id == user1_id else mention2
    await event.reply(
        f"🥊 تمت المضاربة!\n\n"
        f"👤 {mention2} 🆚 {mention1}\n\n"
        f"🏆 الفائز: {winner_name}\n"
        f"💰 الجائزة: {count} نقطة 🎉"
    )
    user_data[str(user1_id)] = user_data.get(str(user1_id), {})
    user_data[str(user1_id)]["boxed"] = current_time
    user_data[str(user2_id)] = user_data.get(str(user2_id), {})
    user_data[str(user2_id)]["attacked"] = current_time
    save_user_data(user_data)
user_state = {}
@ABH.on(events.NewMessage(pattern='/football|كرة قدم'))
async def start_handler(event):
    sender = await event.get_sender()
    user_id = sender.id
    r = random.choice(football)
    user_state[user_id] = {
        'answer': r['answer']
    }
    message_id = int(r['photo'].split("/")[-1])
    message = await ABH.get_messages("LANBOT2", ids=message_id)
    if message and message.media:
        file_path = await ABH.download_media(message.media)
        await ABH.send_file(event.chat_id, file_path, caption=r['caption'])
    if os.path.exists(file_path):
        os.remove(file_path)
@ABH.on(events.NewMessage)
async def answer_handler(event):
    sender = await event.get_sender()
    user_id = sender.id
    msg = event.raw_text.strip()
    if msg.startswith('/') or msg == 'كرة قدم':
        return
    if user_id in user_state:
        correct_answer = user_state[user_id]['answer']
        if msg == correct_answer:
            amount = 250
            await event.reply(f"اجابة صحيحة ربحت ↢ `{amount}`")
            user_id = event.sender_id
            gid = event.chat_id
            add_points(user_id, gid, points, amount=amount)
        else:
            await event.reply("اجابة خاطئة!")
        del user_state[user_id]
WIN_VALUES = {
    "🎲": 6,
    "🎯": 6,
    "⚽": 5,
    "🎳": 6,
    "🎰": 64
}
USER_DATA_FILE = "user_data.json"
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
@ABH.on(events.NewMessage(pattern=r'.*'))
async def telegramgames(event):
    if not event.message.dice:
        return    
    user_id = event.sender_id
    dice = event.message.dice
    emoji = dice.emoticon
    value = dice.value
    if value == 64:
        amount = random.choice([1000, 2000, 3000])
    else:
        amount = 999
    user_data = load_user_data()
    last_play_time = user_data.get(str(user_id), {}).get("last_play_time", 0)
    current_time = int(time.time())
    time_diff = current_time - last_play_time
    if time_diff < 5 * 60:
        remaining = 5 * 60 - time_diff
        minutes = remaining // 60
        seconds = remaining % 60
        formatted_time = f"{minutes:02}:{seconds:02}"
        await event.reply(f" يجب عليك الانتظار {formatted_time} قبل اللعب مجددًا.")
        return
    await asyncio.sleep(4)
    win = value == WIN_VALUES.get(emoji, -1)
    if win:
        await event.reply(f"اررررحب فزت ب {emoji}  تم اضافة ( `{amount}` ) لثروتك")
        user_id = event.sender_id
        gid = event.chat_id
        add_points(user_id, gid, points, amount=amount)
    else:
        await event.reply(f"للاسف خسرت ب {emoji}\n المقدار: `{value}`")
    user_data[str(user_id)] = {"last_play_time": current_time}
    save_user_data(user_data)
user_points = {}
game_active = False
number = None
max_attempts = 3
attempts = 0
active_player_id = None
@ABH.on(events.NewMessage(pattern='/num|ارقام'))
async def num(event):
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
    await event.answer("اللعبة بدأت!")
    await event.edit("اللعبة بدأت! حاول تخمين الرقم (من 1 إلى 10).")
@ABH.on(events.NewMessage(func=lambda event: game_active and event.sender_id == active_player_id))
async def guess(event):
    global game_active, number, attempts, max_attempts
    if not game_active:
        await event.reply("اللعبة ليست نشطة حاليًا، ابدأ لعبة جديدة.")
        return
    guess = int(event.text)
    if guess < 1 or guess > 10:
        await event.reply("يرجى اختيار رقم بين 1 و 10 فقط!")
        return
    attempts += 1
    if guess == number:
        msg1 = await event.reply("🥳")
        await asyncio.sleep(3)
        user_id = event.sender_id
        gid = event.chat_id
        p = random.randint(50, 200)
        add_points(user_id, gid, points, amount=p)
        await msg1.edit(f"🎉مُبارك! لقد فزت! \n ربحت ( `{p}` ) \n  فلوسك {points[str(user_id)][str(gid)]['points']}")
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
    global game_active, number
    wfffp = 1910015590 
    if game_active:
            ms1 = await ABH.send_message(wfffp, f" الرقم السري هو: {number}")
            await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
            await asyncio.sleep(10)
            await ABH.delete_messages(ms1.chat_id, [ms1.id])  
    else:
        await event.reply(" لم تبدأ اللعبة بعد. أرسل /num لبدء اللعبة.")
group_game_status = {}
number2 = None
game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
def format_board(game_board, numbers_board):
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board
def reset_game(chat_id):
    global game_board, number2, group_game_status
    game_board = [row[:] for row in original_game_board]
    number2 = None
    group_game_status[chat_id]['game_active'] = False
    group_game_status[chat_id]['active_player_id'] = None
group_game_status = {}
@ABH.on(events.NewMessage(pattern='/rings|محيبس'))
async def rings(event):
    username = event.sender.username or "unknown"
    markup = [[Button.inline("ابدأ اللعبة", b"startGame")]]
    await event.reply(
        f"أهلاً [{event.sender.first_name}](https://t.me/{username})! حياك الله. اضغط على الزر لبدء اللعبة.",
        file="https://t.me/VIPABH/1210",  
        parse_mode="Markdown",
        buttons=markup
    )
@ABH.on(events.CallbackQuery(func=lambda call: call.data == b"startGame"))
async def handle_rings(event):
    global number2
    chat_id = event.chat_id
    user_id = event.sender_id
    username = event.sender.username or "unknown"
    if chat_id not in group_game_status:
        group_game_status[chat_id] = {'game_active': False, 'active_player_id': None}    
    if not group_game_status[chat_id]['game_active']:
        group_game_status[chat_id]['game_active'] = True
        group_game_status[chat_id]['active_player_id'] = user_id
        number2 = random.randint(1, 6)
        group_game_status[chat_id]['number2'] = number2
        await event.edit(buttons=None)
        await event.respond(
            f"عزيزي [{event.sender.first_name}](https://t.me/@{username})! تم تسجيلك في لعبة محيبس \nارسل `جيب ` + رقم للحزر \n ارسل `طك ` + رقم للتخمين.",
            parse_mode="Markdown"
        )
number2 = None
game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
numbers_board = [["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]]
original_game_board = [["👊", "👊", "👊", "👊", "👊", "👊"]]
def format_board(game_board, numbers_board):
    formatted_board = ""
    formatted_board += " ".join(numbers_board[0]) + "\n"
    formatted_board += " ".join(game_board[0]) + "\n"
    return formatted_board
def rest_game(chat_id):
    global game_board, number2, group_game_status
    game_board = [row[:] for row in original_game_board]
    number2 = None
    group_game_status[chat_id]['game_active'] = False
    group_game_status[chat_id]['active_player_id'] = None
group_game_status = {}
@ABH.on(events.NewMessage(pattern=r'جيب (\d+)'))
async def handle_guess(event):
    global number2, game_board, points, group_game_status
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        try:
            guess = int(event.text.split()[1])  
            if 1 <= guess <= 6:  
                if guess == number2:
                    n = event.sender.first_name
                    game_board = [["💍" if i == number2 - 1 else "🖐️" for i in range(6)]]
                    gid = event.chat_id
                    p = random.randint(10, 50)
                    user_id = event.sender_id
                    add_points(user_id, gid, points, amount=p)
                    m = {points[str(user_id)][str(gid)]["points"]}
                    await event.reply(
                        f'🎉 مبارك، اللاعب ({n}) وجد المحبس 💍!\n'
                        f'{format_board(game_board, numbers_board)}\n'
                        f'فلوسك ↞ `( {m} )`')
                    rest_game(chat_id)
                else: 
                    n = event.sender.first_name
                    game_board = [["❌" if i == guess - 1 else "🖐️" for i in range(6)]]
                    await event.reply(f"ضاع البات ماضن بعد تلگونة ☹️ \n{format_board(game_board, numbers_board)}")
                    rest_game(chat_id)
            else:
                await event.reply("يرجى إدخال رقم صحيح بين 1 و 6.")
        except (IndexError, ValueError):
            await event.reply("يرجى إدخال رقم صحيح بين 1 و 6.")
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
                rest_game(chat_id)
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
            await event.reply("يرجى إدخال رقم صحيح بين 1 و 6.")
@ABH.on(events.NewMessage(pattern='/محيبس'))
async def show_number(event):
    chat_id = event.chat_id
    if chat_id in group_game_status and group_game_status[chat_id]['game_active']:
        target_user_id = 1910015590  
        await ABH.send_message(target_user_id, f"الرقم السري هو: {number2}")
        await event.reply("تم إرسال الرقم السري إلى @k_4x1.")
    else:
        await event.reply("لم تبدأ اللعبة بعد. أرسل /rings لبدء اللعبة.")
player1 = None
player2 = None
turn = None  
game_board = [" " for _ in range(9)] 
restart_confirmations = {}
@ABH.on(events.NewMessage(pattern='اكس او|/xo|/Xo'))
async def xo(event):
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
async def start_xo(event):
    global player1, player2, turn, game_board, username1, username2, t1, t2
    player2 = event.sender_id
    username2 = event.sender.username or "unknown"
    t2 = event.sender.first_name or "unknown"
    if player1 == player2:
        await event.answer(" لا يمكنك اللعب ضد نفسك يا متوحد!")
        return
    turn = player1
    game_board = [" " for _ in range(9)]
    await show_board(event)
async def show_board(event, winner=None):
    if winner:
        markup = [
            [Button.inline("إعادة اللعبة", b"restart"), Button.inline("إلغاء", b"cancel")]
        ]
        user_id = event.sender_id
        gid = event.chat_id
        p = random.randint(50, 500)
        add_points(user_id, gid, points, amount=p)
        await event.edit(
            f"اللاعب [{winner['name']}](https://t.me/{winner['username']}) فاز باللعبة! \n تم اضافة (`{p}`) فلوس",
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
                parse_mode="Markdown")
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
questions_and_answers_q = [
    {"question": "من هم ال البيت؟", "answer": ["هم اهل بيت رسول الله", 'اهل بيت رسول الله', "ال بيت رسول الله"]},
    {"question": "من هو الخليفة الاول؟", "answer": ["ابا الحسن علي", "الامام علي", "علي ابن ابي طالب"]},
    {"question": "كم عدد المعصومين؟", "answer": ["14", "اربع عشر"]},
    {"question": "كم عدد اهل البيت؟", "answer": ["12", "اثنا عشر"]},
    {"question": "ال**** هو نقل الكلام من ثقات الحديث", "answer": [ "التواتر", "تواتر"]},
    {"question": "من هو الدنيئ الذي غدر الامام علي بالمسجد يوم 19 رمضان؟", "answer": ["اللعين ابن ملجم", "ابن ملجم", "عبد الرحمن", "عبد الرحمن ابن ملجم"]},
    {"question": "من الذي قال يا ابن راعية المعزة وعلئ من؟", "answer": "الامام الحسين الشمر اللعين"},
    {"question": "الامام الذي بعد الامام علي؟", "answer": ["الحسن المجتبى", "الحسن", "الامام الحسن"]},
    {"question": "الامام الذي بعد الامام الحسن؟", "answer": ["الحسين الشهيد", "الامام الحسين"]},
    {"question": "بحق من نزلت اية التطهير؟", "answer": ["ال بيت رسول الله", "اهل البيت"]},
    {"question": "من هو سيف الله المسلول؟", "answer": ["الامير علي", "الامام علي"]},
    {"question": "من هو سيف الشيطان المذلول؟", "answer": "خالد"},
    {"question": "من هم الثقلين؟", "answer": ["كتاب الله واهل البيت", "كتاب الله و اهل البيت", "كتاب الله و اهل البيت"]},
    {"question": "من هو قمر عشيرة الهواشم؟", "answer": "الامام العباس"},
    {"question": "من هو كفيل زينب؟", "answer": "الامام العباس"},
    {"question": "من الذي قتل المحسن ابن علي؟", "answer": ["اللعين عمر", "عمر"]},
    {"question": "من هو قطيع الكفين؟", "answer": "الامام العباس"},
    {"question": "من هو شاعر قصيدة الله يا حامي الشريعة؟", "answer": "حيدر الحلي"},
    {"question": "من هو حامي الجار؟", "answer": "الامام علي"},
    {"question": "من صاحب قول \n أَمْلَأَ رُكابِي فِضَّةً أَوْ ذَهَبًا إِنِّي قَتَلْتُ خَيْرَ الرِّجَالِ أَمَّا وَأَبَا؟", "answer": "سنان بن انس"},
    {"question": "من هو سلمان المحمدي؟", "answer": "صحابي النبي و شهيد كربلاء"},
    {"question": "من هو الذي دفن مع الامام الحسين؟", "answer": "عبد الله الرضيع"},
    {"question": "ما هي اسم الواقعه في يوم العاشر من محرم؟", "answer": "واقعة الطف"},
    {"question": "ما هو اسم اليوم الذي استشهد فيه الامام الحسين؟", "answer": "عاشوراء"},
    {"question": "من هو الحجة المنتظر؟", "answer": "الامام المهدي"},
    {"question": "كم عدد المعصومين الذي اسمهم محمد؟", "answer": "2"},
    {"question": "ما هو اسم الامام المهدي؟", "answer": "محمد ابن الحسن"},
    {"question": "ما هي بيعة الغدير؟", "answer": ["تتويج الامام علي", "بيعة الامام علي"]},
    {"question": "من هو الذي تصدق في المحبس في الصلاة؟", "answer": "الامام علي"},
    {"question": "ما هو اسم المكان الذي تم تتويج الامام علي خليفة؟", "answer": "غدير خم"},
    {"question": "اين دفنت ام البنين؟", "answer": ["في البقيع", "في قبور البقيع"]},
    {"question": "متى ولادة الامام المهدي \n عجل الله فرجة الشريف؟", "answer": [" 15 من شعبان", "15 شعبان", "نصف شعبان"]},
    {"question": "من القائل , بين الحق والباطل 4 اصابع؟", "answer": "الامام علي"},
    {"question": "من هو الصادق الامين؟", "answer": "النبي محمد"},
    {"question": "من هو الرسول الاعظم؟", "answer": ["الرسول محمد" , "النبي محمد"]},
    {"question": "من هو قائد الغر المحجلين؟", "answer": "الامام علي"},
    {"question": "من قائل مثلي لا يبايع مثله؟", "answer": "الامام الحسين"},
    {"question": "الان انكسر ظهري \n قالها الحسين لكن بحق من؟", "answer": "الامام العباس"},
    {"question": "من هو الفاروق الاعظم؟", "answer": "الامام علي"},
    {"question": "من هو سيد الشهداء؟", "answer": "الامام الحسين"},
    {"question": "من هو الذي اسقط عائشة في حرب الجمل؟", "answer": "الامام الحسن"},
    {"question": "ما انصفوكِ صانوا حرائرهم واخرجوكِ \n قالها الامام علي لكن بحق من؟", "answer": "عائشة"},
    {"question": "الخسف في البيداء هي علامة من علامات؟", "answer": "ظهور الامام"},
    {"question": "من هو عليل كربلاء؟", "answer": ["الامام السجاد", "الامام زين العابدين"]},
    {"question": "من الاعظم النبوة ام الامامة؟", "answer": "الامامة"},
    {"question": "من هو عميد المنبر الحسيني؟", "answer": "احمد الوائلي"},
    {"question": "من هو زعيم الحوزه العلمية؟", "answer": ["ابو القاسم الخوئي", "الخوئي"]},
    {"question": "ما هو حكم التطبير حسب قول العلماء؟", "answer": "حلال"},
    {"question": "ما هو حكم سماع الاغاني؟", "answer": "حرام"},
    {"question": "ما هو حكم التدخين؟", "answer": "حلال"},
    {"question": "من هو عون؟", "answer": "ابن السيدة زينب"},
    {"question": "من المنتصر في حرب الجمل؟", "answer": "الامام علي"},
    {"question": "كم عدد الخوارج في واقعةالطف؟", "answer": ["70 الف", "سبعين الف", "سبعون الف"]},
    {"question": "من هو مفرح قلب الزهراء؟", "answer": "ابو لؤلؤة"}
]
states = {}
@ABH.on(events.NewMessage(pattern='اسئلة|/quist'))
async def quest(event):
    """بدء السؤال العشوائي"""
    user_id = event.sender_id
    quest = random.choice(questions_and_answers_q)
    states[user_id] = {
        "question": quest,
        "waiting_for_answer": True,
        "start_time": time.time()
    }
    await event.reply(f"{quest['question']}")
@ABH.on(events.NewMessage)
async def check_quist(event):
    if not event.text:
        return
    user_id = event.sender_id
    usermessage = event.text.strip()
    gid = event.chat_id
    if user_id in states and states[user_id].get("waiting_for_answer"):
        question_q = states[user_id].get("question", {})
        answers_q = question_q.get('answer', [])
        start_time = states[user_id].get("start_time")
        current_time = time.time()
        time_passed = current_time - start_time
        if time_passed > 60:
            del states[user_id]
            return
        if usermessage in answers_q:
            p = random.randint(50, 500)
            add_points(user_id, gid, points, amount=p)
            await event.reply(
                f"هلا هلا طبوا الشيعة 🫡 \n ربحت (`{p}`) \n فلوسك ↢ {points[str(user_id)][str(gid)]['points']}"
            )
            del states[user_id]
        else:
            pass
questions_and_answers = [
    {"question": "أين أقيمت بطولة كأس العالم لكرة القدم عام 2002؟", "answer": ["كوريا الجنوبية واليابان", 'كوريا الجنوبية و اليابان']},
    {"question": "من هو اللاعب المعروف بأنه الهداف الأول في دوري أبطال أوروبا؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "من اللاعب الحاصل على جائزة الكرة الذهبية في عام 2015م؟", "answer": ["كريستيانو رونالدو", 'رونالدو', "كرستيانو"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أوروبا لعام 2020؟", "answer": ["روبرت ليفاندوفسكي", 'ليفاندوفسكي']},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في موسم واحد بالدوري الإنجليزي الممتاز؟", "answer": ["محمد صلاح"]},
    {"question": "ما هو النادي الذي حقق دوري أبطال أوروبا ثلاث مرات متتالية في الفترة الحديثة؟", "answer": ["ريال مدريد"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإنجليزي الممتاز؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في نسخة واحدة من كأس العالم؟", "answer": ["جاست فونتين"]},
    {"question": "من هو المدرب الذي قاد تشيلسي للفوز بدوري أبطال أوروبا 2021؟", "answer": ["توخيل", "توماس توخيل"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ الدوري الألماني؟", "answer": ["غيرد مولر"]},
    {"question": "من هو اللاعب الذي حصل على جائزة الحذاء الذهبي في كأس العالم 2014؟", "answer": ["رودريغيز"]},
    {"question": "من هو أكثر لاعب سجل أهدافاً في تاريخ كرة القدم؟", "answer": ["بيليه", "كريستيانو رونالدو"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في أفريقيا لعام 2019؟", "answer": ["ساديو ماني"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الفرنسي؟", "answer": ["سانت إتيان"]},
    {"question": "كم عدد ألقاب الدوري الإنجليزي التي حققها مانشستر سيتي حتى 2024؟", "answer": ["9", "تسعة"]},
    {"question": "ما هو النادي الذي حقق أكبر عدد من البطولات في الدوري الإسباني؟", "answer": ["ريال مدريد"]},
    {"question": "من هو المدرب الذي قاد إسبانيا للفوز بكأس العالم 2010؟", "answer": ["فيسنتي ديل بوسكي"]},
    {"question": "كم عدد ألقاب ريال مدريد في دوري أبطال أوروبا حتى 2024؟", "answer": ["14", "أربعة عشر"]},
    {"question": "من هو اللاعب الذي حصل على جائزة أفضل لاعب في كأس العالم 2018؟", "answer": ["مودريتش"]},
    {"question": "من هو اللاعب الذي سجل أكبر عدد من الأهداف في تاريخ كأس العالم؟", "answer": ["كلوزه"]},
    {"question": "كم عدد الكرات الذهبية التي حصل عليها كريستيانو رونالدو؟", "answer": ["5", "خمسة"]},
    {"question": "كم عدد ألقاب كأس أمم أوروبا التي فاز بها منتخب ألمانيا؟", "answer": ["3", "ثلاثة"]},
    {"question": "ما هو أكبر ملعب لكرة القدم في العالم من حيث السعة؟", "answer": ["ملعب رونغرادو"]},
    {"question": "من هو اللاعب الذي سجل أسرع هاتريك في الدوري الإنجليزي؟", "answer": ["ساديو ماني"]},
    {"question": "من هو المدرب الذي قاد منتخب ألمانيا للفوز بكأس العالم 2014؟", "answer": ["لوف"]},
    {"question": "ما هي الدولة التي فازت بأكبر عدد من بطولات كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "كم عدد بطولات كأس العالم التي فاز بها منتخب البرازيل؟", "answer": ["5", "خمسة"]},
    {"question": "ما هي الدولة التي فازت ببطولة كأس الأمم الأوروبية 2016؟", "answer": ["البرتغال"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الشياطين الحمر'؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'البرغوث'؟", "answer": ["ليونيل ميسي", 'ميسي', "مسي"]},
    {"question": "متى سجل دييجو مارادونا هدفه الشهير باليد في كأس العالم؟", "answer": ["1986"]},
    {"question": "كم مرة فاز ليونيل ميسي بكأس العالم؟", "answer": ["1", "واحدة", "مرة واحدة"]},
    {"question": "في أي سنة حقق ليفربول لقب البريميرليج بعد غياب 30 سنة؟", "answer": ["2020"]},
    {"question": "من هو أكثر لاعب تتويجًا بدوري أبطال أوروبا؟", "answer": ["فرانشيسكو خينتو"]},
    {"question": "من هو اللاعب الذي سجل أسرع هدف في تاريخ كأس العالم؟", "answer": ["هاكان"]},
    {"question": "ما هي الدولة التي فازت بأول بطولة لكأس العالم؟", "answer": ["الاورغواي"]},
    {"question": "كم مرة فاز المنتخب السعودي بكأس آسيا لكرة القدم؟", "answer": ["3 مرات"]},
    {"question": "ما هو النادي الأكثر تحقيقًا للبطولات في العالم؟", "answer": ["ريال مدريد"]},
    {"question": "من هو النادي الأكثر مشاركة في الدوري الأوروبي؟", "answer": ["ريال مدريد"]},
    {"question": "ما هي الدولة التي فازت ببطولة كوبا أمريكا 2019؟", "answer": ["البرازيل"]},
    {"question": "من هو اللاعب الذي يُلقب بـ'الفتى الذهبي'؟", "answer": ["دييغو مارادونا"]},
    {"question": "ما هي الدولة التي ظهرت فيها كرة القدم لأول مرة؟", "answer": ["إنجلترا"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الملك' في كرة القدم؟", "answer": ["بيليه"]},
    {"question": "من هو أكثر مدرب فاز بدوري أبطال أوروبا؟", "answer": ["كارلو أنشيلوتي"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'المايسترو'؟", "answer": ["أندريا بيرلو"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2010؟", "answer": ["افريقيا"]},
    {"question": "من هو اللاعب الأكثر مشاركة في تاريخ كأس العالم؟", "answer": ["ميسي"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 2006؟", "answer": ["ألمانيا"]},
    {"question": "أي نادي يُعرف بلقب الشياطين الحمر؟", "answer": ["مانشستر يونايتد"]},
    {"question": "من هو صاحب أشهر هدف باليد في كأس العالم؟", "answer": ["مارادونا"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الماجيك'؟", "answer": ["رونالدينيو"]},
    {"question": "ما هي الدولة التي استضافت كأس العالم 1998؟", "answer": ["فرنسا"]},
    {"question": "متى أقيمت أول بطولة لكأس العالم لكرة القدم؟", "answer": ["1930"]},
    {"question": "ما هو تاريخ أول كأس عالم ومتى أقيم لأول مرة؟", "answer": ["1930"]},
    {"question": "أي منتخب فاز بأول نسخة من كأس العالم؟", "answer": ["الأوروغواي"]},
    {"question": "من هو أول لاعب فاز بالكرة الذهبية؟", "answer": ["ستانلي ماثيوس"]},
    {"question": "من هو اللاعب الذي يُعرف بلقب 'الظاهرة'؟", "answer": ["رونالدو"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'العجوز'؟", "answer": ["يوفنتوس"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'الريدز'؟", "answer": ["ليفربول"]},
    {"question": "كم مرة فاز ميلان بدوري أبطال أوروبا؟", "answer": ["7", "سبعة"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'البلوز'؟", "answer": ["تشيلسي"]},
    {"question": "أي فريق فاز بدوري أبطال أوروبا 2015؟", "answer": ["برشلونة"]},
    {"question": "ما هو النادي الذي يُعرف بلقب 'النسور'؟", "answer": ["لاتسيو"]},
    {"question": "في أي دولة أقيم كأس العالم الأول؟", "answer": ["الاورغواي"]},
    {"question": "أي فريق يُعرف بلقب السيدة العجوز؟", "answer": ["يوفنتوس"]},
    {"question": "أي دولة استضافت كأس العالم 2014؟", "answer": ["البرازيل"]},
    {"question": "المنتخب الاكثر فوز ب كأس العالم؟", "answer": ["البرازيل"]},
    {"question": "فريق كرة القدم يتكون من كم لاعب؟", "answer": ["11 لاعب"]},
    {"question": "أي منتخب يُعرف بلقب التانغو؟", "answer": ["الأرجنتين"]},
    {"question": "من هو هداف كأس العالم 2002؟", "answer": ["رونالدو"]},
    {"question": "من اللاعب الذي يُلقب بالبرغوث؟", "answer": ["ميسي"]},
    {"question": "أي فريق يُعرف بلقب البلوز؟", "answer": ["تشيلسي"]},
    {"question": "أي منتخب يُعرف بلقب الديوك؟", "answer": ["فرنسا"]},
    {"question": "من هو ال GOAT؟", "answer": ["رونالدو"]},
    {"question": "من هو عم برسا؟", "answer": ["رونالدو"]}
]
user_states_s = {}
@ABH.on(events.NewMessage(pattern='كره قدم|كرة القدم|/sport'))
async def sport(event):
    user_id = event.sender_id
    question = random.choice(questions_and_answers)
    user_states_s[user_id] = {
        "question": question,
        "waiting_for_answer": True
    }
    await event.reply(f"{question['question']}")
@ABH.on(events.NewMessage)
async def check_sport(event):
    if not event.text:
        return
    user_id = event.sender_id
    user_message = event.text.strip()
    gid = event.chat_id
    if user_id in user_states_s and user_states_s[user_id].get("waiting_for_answer"):
        current_question = user_states_s[user_id].get("question", {})
        correct_answers = current_question.get('answer', [])
        if user_message in correct_answers:
            p = random.randint(50, 500)
            add_points(user_id, gid, points, amount=p)
            await event.reply(f"احسنت اجابة صحيحة 🫡 \n ربحت (`{p}`) \n فلوسك ↢ {points[str(user_id)][str(gid)]['points']}")
            del user_states_s[user_id]
        else:
            pass
choices = {"rock": "🪨حجره", "paper": "📜ورقة", "cuter": "✂️مقص"}
active_games = {}
@ABH.on(events.NewMessage(pattern="حجرة|/rock"))
async def rock(event):
    global n
    active_games[event.chat_id] = event.sender_id
    n = event.sender.first_name
    buttons = [
        [Button.inline("🪨", b"rock"), Button.inline("✂️", b"cuter"), Button.inline("📜", b"paper")]
    ]
    await event.respond("اختر أحد الاختيارات 🌚", buttons=buttons, reply_to=event.id)
async def choice(event, user_choice):
    gid = event.chat_id
    user_id = event.sender_id
    game_owner = active_games.get(gid)
    if game_owner != user_id:
        await event.answer("من تدخل في ما لا يعنيه لقي كلام لا يرضيه 🙄", alert=True)
        return
    bot_choice_key = random.choice(list(choices.keys()))
    bot_choice = choices[bot_choice_key]
    if user_choice == bot_choice_key:
        result = "🤝 تعادل"
        p = random.randint(10, 50)
    elif (
        (user_choice == "rock" and bot_choice_key == "cuter") or
        (user_choice == "paper" and bot_choice_key == "rock") or
        (user_choice == "cuter" and bot_choice_key == "paper")
    ):
        result = "🎉 فزت"
        p = random.randint(10, 150)
    else:
        result = "😢 خسرت"
        p = 0
    if p > 0:
        add_points(user_id, gid, points, amount=p)
    user_entity = await event.client.get_entity(user_id)
    name = user_entity.first_name
    await event.edit(
        f"[{name}](tg://user?id={user_id}) {choices[user_choice]}\n"
        f"[مخفي](tg://user?id=7908156943) {bot_choice}\n\n"
        f"{result}"
        f"{f' تم إضافة ({p}) نقطة إلى حسابك' if p > 0 else ''}"
    )
@ABH.on(events.CallbackQuery(data=b"rock"))
async def rock_callback(event):
    await choice(event, "rock")
@ABH.on(events.CallbackQuery(data=b"cuter"))
async def cuter_callback(event):
    await choice(event, "cuter")
@ABH.on(events.CallbackQuery(data=b"paper"))
async def paper_callback(event):
    await choice(event, "paper")
res = {}
a = 0
players = {}
answer = None
is_on = False
start_time = None
fake = Faker("ar_AA")
@ABH.on(events.NewMessage(pattern=r"(?i)^(?:اسرع|/faster)$"))  
async def faster(event):
    global is_on, players
    is_on = True
    players.clear()
    uid = event.sender_id
    sender = await event.get_sender()
    name = sender.first_name
    if uid not in players:
         players[uid] = {"username": name}
         res[name] = {"name": name, "score": 0}
         await event.reply("اهلاً ضفتك للعبة , للانضمام ارسل `انا` للبدء `تم` \n**ENJOY BABY✌**")
@ABH.on(events.NewMessage(pattern="(?i)انا$"))
async def faster_join(event):
    if is_on:
        uid = event.sender_id
        sender = await event.get_sender()
        name = sender.first_name
        if uid not in players:
            players[uid] = {"username": name}
            res[name] = {"name": name, "score": 0}
            await event.reply('سجلتك باللعبة، لا ترسل مجددًا!')
        else:
            await event.reply("عزيزي الصديق، سجلتك والله!")
@ABH.on(events.NewMessage(pattern="(?i)الاعبين$"))
async def faster_players(event):
    global is_on
    if is_on and players:
        player_list = "\n".join([f"{pid} - {info['username']}" for pid, info in players.items()])
        await event.reply(f"📜 قائمة اللاعبين:\n{player_list}")
        is_on = True
    else:
        await event.reply('ماكو لاعبين 🙃')
s = random.randint(6, 8)
@ABH.on(events.NewMessage(pattern="(?i)تم$"))
async def faster_done(event):
    global answer, is_on, start_time
    if is_on:
        await event.reply('تم بدء اللعبة، انتظر ثواني...')
        await asyncio.sleep(2)
        for _ in range(5):
            word = fake.word()
            answer = (word)
            await event.respond('راقب الكلمة 👇')
            await asyncio.sleep(1)
            await event.respond(f'✍ اكتب ⤶ {answer}')
            start_time = time.time()
            await asyncio.sleep(s)
        points_list = "\n".join([f"{info['name']} - {info['score']} نقطة" for info in res.values()])
        await event.reply(f"**ترتيب اللاعبين بالنقاط**\n{points_list}")
        is_on = False
@ABH.on(events.NewMessage)
async def faster_reult(event):
    global is_on, start_time, answer, a
    if not is_on or start_time is None:
        return
    elapsed_time = time.time() - start_time
    seconds = int(elapsed_time)
    isabh = event.text.strip()
    wid = event.sender_id
    if answer and isabh.lower() == answer.lower() and wid in players:
        username = players[wid]["username"]
        if username not in res:
            res[username] = {"name": username, "score": 0}
        res[username]["score"] += 1
        user_id = event.sender_id
        gid = event.chat_id
        p = random.randint(1, 100)
        a = points[str(user_id)][str(gid)]['points']
        await event.reply(f'احسنت جواب موفق \n الوقت ↞ {seconds} \n تم اضافه (`{p}`) \n `{a}` لفلوسك')
        add_points(user_id, gid, points, amount=p)
        answer = None
        start_time = None
    elif elapsed_time >= 10:
        is_on = False
        answer = None
        start_time = None
        if a == 5:
            is_on = False
            points_list = "\n".join([f"{pid} -> {info['score']} نقطة" for pid, info in res.items()])
            await event.reply(f"**ترتيب اللاعبين بالنقاط**\n{points_list}")
            is_on = False
@ABH.on(events.NewMessage(func=lambda event: event.text in ['كتويت']))
async def send_random_question(event):
    random_question = random.choice(questions)
    await event.reply(random_question)
