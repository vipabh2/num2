from telethon.tl.types import DocumentAttributeAudio
from telethon import events, Button
from yt_dlp import YoutubeDL
import os, asyncio, json
from other import botuse, is_assistant
from ABH import ABH
import os
import json
def isc(chat_id: int, key: str) -> bool:
    data = {}
    if os.path.exists("locks.json"):
        with open("locks.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return False
    chat_id_str = str(chat_id)
    return data.get(chat_id_str, {}).get(key, False)
COOKIES_FILE = 'c.txt'
if not os.path.exists("downloads"):
    os.makedirs("downloads")
CACHE_FILE = "audio_cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        audio_cache = json.load(f)
else:
    audio_cache = {}
def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(audio_cache, f, ensure_ascii=False, indent=2)
YDL_OPTIONS = {
    'format': 'bestaudio/best',  # أفضل صيغة صوتية متاحة
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'cookiefile': COOKIES_FILE,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
    'default_search': 'ytsearch',
}

def get_valid_audio_format(video_info):
    if 'formats' not in video_info:
        return None
    for fmt in video_info['formats']:
        if fmt.get('acodec') != 'none' and fmt.get('url'):
            return fmt['format_id']
    return None

@ABH.on(events.NewMessage(pattern=r'^.(يوت|yt) (.+)'))
async def download_audio(event):
    if isc(event.chat_id, "اليوتيوب"):
        return
    query = event.pattern_match.group(2)
    chat_id = event.chat_id
    button = Button.url('CHANNEL', 'https://t.me/X04OU')
    try:
        ydl = YoutubeDL(YDL_OPTIONS)
        search_result = await asyncio.to_thread(ydl.extract_info, f"ytsearch:{query}", download=False)
        if 'entries' not in search_result or not search_result['entries']:
            await event.reply("❌ لم يتم العثور على نتائج.")
            return

        video_info = search_result['entries'][0]

        audio_format = get_valid_audio_format(video_info)
        if not audio_format:
            await event.reply("⚠️ لا توجد صيغة صوتية صالحة للتحميل.")
            return

        ydl_opts = YDL_OPTIONS.copy()
        ydl_opts['format'] = audio_format
        ydl_download = YoutubeDL(ydl_opts)
        download_info = await asyncio.to_thread(ydl_download.extract_info, f"ytsearch:{query}", download=True)

        downloaded_video = download_info['entries'][0]
        file_path = ydl_download.prepare_filename(downloaded_video).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        await ABH.send_file(
            chat_id,
            file=file_path,
            caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
            attributes=[
                DocumentAttributeAudio(
                    duration=downloaded_video.get("duration", 0),
                    title=downloaded_video.get("title"),
                    performer='ANYMOUS'
                )
            ],
            buttons=[button],
            reply_to=event.message.id
        )
    except Exception as e:
        await event.reply(f"حدث خطأ: {e}")
    #         await ABH.send_file(
    #             c,
    #             file=val["file_id"],
    #             caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
    #             attributes=[
    #                 DocumentAttributeAudio(
    #                     duration=val.get("duration", 0),
    #                     title=val.get("title"),
    #                     performer='ANYMOUS'
    #                 )
    #             ],
    #             buttons=[b],
    #             reply_to=event.message.id
    #         )
    #         return
    #     download_info = await asyncio.to_thread(ydl.extract_info, f"ytsearch:{query}", download=True)
    #     downloaded_video = download_info['entries'][0]
    #     file_path = ydl.prepare_filename(downloaded_video).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    #     msg = await ABH.send_file(
    #         c,
    #         file=file_path,
    #         caption="[ENJOY DEAR](https://t.me/VIPABH_BOT)",
    #         attributes=[
    #             DocumentAttributeAudio(
    #                 duration=downloaded_video.get("duration", 0),
    #                 title=downloaded_video.get("title"),
    #                 performer='ANYMOUS'
    #             )
    #         ],
    #         buttons=[b],
    #         reply_to=event.message.id
    #     )
    #     audio_cache[downloaded_video.get("id")] = {
    #         "file_id": msg.file.id,
    #         "title": downloaded_video.get("title"),
    #         "duration": downloaded_video.get("duration", 0),
    #         "query": query
    #     }
    #     save_cache()
    # except Exception as e:
    #     await ABH.send_message(1910015590, f"Error: {str(e)}")
@ABH.on(events.NewMessage(pattern='^اضف كوكيز$', from_users=[1910015590]))
async def add_cookie(event):
    type = "كوكيز"
    await botuse(type)
    r = await event.get_reply_message()
    if not r or not r.document:
        return await event.reply("❗️يرجى الرد على رسالة تحتوي على ملف كوكيز.")    
    tmp_file = "temp_cookie.txt"
    await r.download_media(file=tmp_file)
    with open(tmp_file, "r", encoding="utf-8") as f:
        content = f.read()
    os.remove(tmp_file)
    if os.path.exists("cookie.json"):
        os.remove("cookie.json")
    with open("cookie.json", "w", encoding="utf-8") as f:
        json.dump({"cookie_data": content}, f, ensure_ascii=False, indent=2)
    await event.reply(" تم حفظ الكوكيز داخل ملف JSON بنجاح.")
@ABH.on(events.NewMessage(pattern=r'^ال(\w+)\s+(تعطيل|تفعيل)$'))
async def handle_flag(event):
    type = "الايدي تفعيل"
    await botuse(type)
    if not is_assistant(event.chat_id, event.sender_id):
        return
    key = event.pattern_match.group(1)
    value_str = event.pattern_match.group(2).lower()
    value = True if value_str == "تفعيل" else False
    type = "قفل او فتح عام"
    await botuse(type)
    data = {}
    if os.path.exists("locks.json"):
        with open("locks.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    if event.chat_id not in data:
        data[event.chat_id] = {}
    data[event.chat_id][key] = value
    with open("locks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    await event.reply(f"تم {value_str} ال{value} بحمده تعالى")
print(COOKIES_FILE)
