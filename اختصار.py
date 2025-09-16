import inspect, os, importlib
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
                func_type = "async" if inspect.iscoroutinefunction(obj) else "normal"
                sig = str(inspect.signature(obj))
                results.append(f"📂 {filename} → 📌 {name} | النوع: {func_type} | المعطيات: {sig}")
    return results
@ABH.on(events.NewMessage(pattern="^الفنكشنات$", from_users=[wfffp]))
async def show_all_functions(event):
    funcs = list_functions_in_folder(".")
    if not funcs:
        await event.reply("لم يتم العثور على أي دوال في ملفات المجلد الحالي.")
    else:
        msg = "📝 قائمة الدوال في المشروع:\n\n" + "\n".join(funcs)
        await event.reply(msg[:4000])
