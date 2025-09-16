from Resources import *
from Program import *
from ABH import *
@ABH.on(evnets.NewMessage)
async def litsin_to_all(e):
  text = e.text
  await som(e)
  # if text == '':
