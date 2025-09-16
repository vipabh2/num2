import inspect, os, importlib, re, json
from telethon import events
from ABH import ABH
from Resources import *
def list_functions_in_folder(folder: str):
    results = []
    for filename in os.listdir(folder):
        if filename.endswith(".py") and filename != os.path.basename(__file__):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                results.append(f"⚠️ فشل تحميل {filename}: {e}")
                continue
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                func_type = "async" if inspect.iscoroutinefunction(obj) else "def"
                sig = str(inspect.signature(obj))
                results.append(f"{func_type} {name}{sig}")
    return results
@ABH.on(events.NewMessage(pattern="^الفنكشنات$", from_users=[wfffp]))
async def show_all_functions(event):
    funcs = list_functions_in_folder(".")
    if not funcs:
        await event.reply("لم يتم العثور على أي دوال في ملفات المجلد الحالي.")
    else:
        msg = "📝 قائمة الدوال في المشروع:\n\n" + "\n".join(f"{i+1}. {f}" for i, f in enumerate(funcs))
        await event.reply(msg[:4000])
def list_patterns_in_folder(folder: str):
    patterns = []
    for filename in os.listdir(folder):
        if filename.endswith(".py") and filename != os.path.basename(__file__):
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = re.findall(r'pattern\s*=\s*[\'"](.+?)[\'"]', content)
                    for m in matches:
                        patterns.append(f"{filename} → {m}")
            except Exception as e:
                patterns.append(f"⚠️ فشل فتح {filename}: {e}")
    return patterns
@ABH.on(events.NewMessage(pattern="^الباترينات$", from_users=[wfffp]))
async def show_all_patterns(event):
    patterns = list_patterns_in_folder(".")
    if not patterns:
        await event.reply("لم يتم العثور على أي باترين في ملفات المجلد الحالي.")
    else:
        msg = "🔍 قائمة الباترينات في المشروع:\n\n" + "\n".join(f"{i+1}. {p}" for i, p in enumerate(patterns))
        await event.reply(msg[:4000])
SHORTCUTS_FILE = "shortcuts.json"
async def امسح(event):
    await event.reply("✅ تم تنفيذ أمر المسح!")
async def بدء(event):
    await event.reply("🎮 تم بدء اللعبة!")
COMMANDS = {
    "امسح": امسح,
    "بدء": بدء
}
def load_shortcuts():
    try:
        with open(SHORTCUTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_shortcuts(data):
    with open(SHORTCUTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
shortcuts = load_shortcuts()
def add_shortcut(main_cmd, shortcut):
    shortcuts[shortcut] = main_cmd
    save_shortcuts(shortcuts)
def remove_shortcut(shortcut):
    if shortcut in shortcuts:
        del shortcuts[shortcut]
        save_shortcuts(shortcuts)
        return True
    return False
@ABH.on(events.NewMessage(pattern="^اضف_اختصار (.+?) (.+)$"))
async def add_shortcut_cmd(event):
    main_cmd, shortcut = event.pattern_match.group(1), event.pattern_match.group(2)
    if main_cmd not in COMMANDS:
        await event.reply(f"❌ لا يوجد أمر أساسي باسم {main_cmd}")
        return
    add_shortcut(main_cmd, shortcut)
    await event.reply(f"✅ تم إضافة الاختصار: {shortcut} للأمر الأساسي: {main_cmd}")
@ABH.on(events.NewMessage(pattern="^احذف_اختصار (.+)$"))
async def remove_shortcut_cmd(event):
    shortcut = event.pattern_match.group(1)
    if remove_shortcut(shortcut):
        await event.reply(f"✅ تم حذف الاختصار: {shortcut}")
    else:
        await event.reply(f"❌ لم يتم العثور على الاختصار: {shortcut}")
@ABH.on(events.NewMessage())
async def handle_shortcuts(event):
    text = event.raw_text.strip()
    if text in shortcuts:
        main_cmd = shortcuts[text]
        if main_cmd in COMMANDS:
            await COMMANDS[main_cmd](event)
