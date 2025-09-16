import inspect, os, importlib, re
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
