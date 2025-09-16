from Resources import *
from program import *
from ABH import *
@ABH.on(evnets.NewMessage)
async def litsin_to_all(e):
  text = e.text
  await som(e)
  # if text == '':
