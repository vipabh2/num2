from telethon import events 
from Resources import *
from Program import *
from count import *
from ABH import *
@ABH.on(events.NewMessage)
async def litsin_to_all(e):
  text = e.text
  await unified_handler(e)
  await som(e)
  await unified_handler(e)
  # if text == '':
@ABH.on(events.CallbackQuery)
async def litson(e):
  await callback_handler(e)
  await callbacklist(e)
@ABH.on(events.InlineQuery)
async def litsonINLIN(e):
  await inlineupdate(e)
