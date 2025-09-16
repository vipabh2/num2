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
SHORTCUTS_FILE="shortcuts.json"
def load_shortcuts():
    try:
        with open(SHORTCUTS_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
def save_shortcuts(data):
    with open(SHORTCUTS_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
shortcuts=load_shortcuts()
def add_shortcut(main,shortcut):
    shortcuts[shortcut]=main
    save_shortcuts(shortcuts)
def remove_shortcut(shortcut):
    if shortcut in shortcuts:
        del shortcuts[shortcut]
        save_shortcuts(shortcuts)
        return True
    return False
COMMANDS={}
for file in os.listdir("."):
    if file.endswith(".py") and file!="run.py":
        module_name=file[:-3]
        try:
            module=importlib.import_module(module_name)
        except:
            continue
        for name,obj in inspect.getmembers(module,inspect.iscoroutinefunction):
            if hasattr(obj,"_events"):
                for e in getattr(obj,"_events"):
                    if isinstance(e,events.NewMessage):
                        pattern=str(e.pattern) if e.pattern else name
                        COMMANDS[pattern]=obj
@ABH.on(events.NewMessage(pattern="^اضف_اختصار (.+?) (.+)$"))
async def add_shortcut_cmd(event):
    main,shortcut=event.pattern_match.group(1),event.pattern_match.group(2)
    if main in COMMANDS:
        add_shortcut(main,shortcut)
        await event.reply(f"تم إضافة الاختصار {shortcut} للأمر {main}")
    else:
        await event.reply(f"❌ لم يتم العثور على الأمر {main}")
@ABH.on(events.NewMessage(pattern="^احذف_اختصار (.+)$"))
async def remove_shortcut_cmd(event):
    s=event.pattern_match.group(1)
    if remove_shortcut(s):
        await event.reply(f"تم حذف الاختصار {s}")
    else:
        await event.reply(f"❌ لم يتم العثور على الاختصار {s}")
@ABH.on(events.NewMessage())
async def handle_shortcuts(event):
    text=event.raw_text.strip()
    if text in shortcuts:
        main=shortcuts[text]
        if main in COMMANDS:
            await COMMANDS[main](event)
import os, importlib, inspect
from telethon import events
from ABH import ABH

async def send_functions_list(folder="."):
    results = []
    for file in os.listdir(folder):
        if file.endswith(".py") and file != os.path.basename(__file__):
            module_name = file[:-3]
            try:
                module = importlib.import_module(module_name)
            except:
                continue
            for name, obj in inspect.getmembers(module, inspect.iscoroutinefunction):
                func_type = "async"
                sig = str(inspect.signature(obj))
                func_name = f"{name}{sig}"
                patterns = []
                if hasattr(obj, "_events"):
                    for e in getattr(obj, "_events"):
                        if isinstance(e, events.NewMessage):
                            patterns.append(str(e.pattern) if e.pattern else None)
                if not patterns:
                    patterns = [None]
                for p in patterns:
                    results.append([func_type, func_name, p])
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                if not inspect.iscoroutinefunction(obj):
                    func_type = "def"
                    sig = str(inspect.signature(obj))
                    func_name = f"{name}{sig}"
                    patterns = []
                    if hasattr(obj, "_events"):
                        for e in getattr(obj, "_events"):
                            if isinstance(e, events.NewMessage):
                                patterns.append(str(e.pattern) if e.pattern else None)
                    if not patterns:
                        patterns = [None]
                    for p in patterns:
                        results.append([func_type, func_name, p])
    return results
@ABH.on(events.NewMessage(pattern="^قائمة_الدوال$", from_users=[wfffp]))
async def show_functions(event):
    funcs = await send_functions_list(".")
    if not funcs:
        await event.reply("لم يتم العثور على أي دوال.")
        return
    msg = "📝 قائمة الدوال:\n\n"
    for i, f in enumerate(funcs, 1):
        type_, name, pattern = f
        pattern_text = pattern if pattern else "لا يوجد"
        msg += f"{i}. {type_} {name} | pattern: {pattern_text}\n"
    await event.reply(msg[:4000])
