spams={}
sessions={}
@ABH.on(events.NewMessage)
async def handler(event):
 try:
  if not event.is_group or event.sender_id!=wfffp or event.sender_id==6520830528:
   return
  sender_id=event.sender_id
  chat_id=event.chat_id
  uid=str(sender_id)
  text=event.raw_text.strip()
  if sender_id in spams:
   d=spams[sender_id]
   if chat_id==d["chat"] and d["stage"]=="active":
    if d["count"]>0:
     await react(event,d["emoji"])
     d["count"]-=1
     if d["count"]<=0:
      await event.reply("تم الانتهاء من الإزعاج")
      del spams[sender_id]
    return
  if text=="ازعاج" and event.is_reply:
   r=await event.get_reply_message()
   target_id=r.sender_id
   if target_id==sender_id:
    await event.reply("لا يمكنك إزعاج نفسك.")
    return
   if uid in points and str(chat_id) in points[uid]:
    user_points=points[uid][str(chat_id)]["points"]
   else:
    await hint("لم يتم العثور على نقاط المستخدم.")
    return
   if user_points<50000:
    await event.reply("ما عندك الفلوس الكافيه علمود تسوي ولو واحد ازعاج")
    return
   sessions[sender_id]={"target":target_id,"stage":"count","chat":chat_id,"user_points":user_points}
   await event.reply("عدد؟")
   return
  if sender_id in sessions:
   sess=sessions[sender_id]
   if sess["chat"]==chat_id and sess["stage"]=="count":
    if text.isdigit() and int(text)>0:
     sess["count"]=int(text)
     x=sess["count"]*50000
     if sess["user_points"]<x:
      h=sess["user_points"]//50000
      await event.reply(f"ما عندك الفلوس الكافيه علمود تسوي ازعاج \n تكدر تسوي ب {h} ازعاج")
      del sessions[sender_id]
      return
     sess["stage"]="emoji"
     await event.reply("الإيموجي؟")
    else:
     await event.reply("أرسل رقم صالح")
    return
   if sess["chat"]==chat_id and sess["stage"]=="emoji":
    target_id=sess["target"]
    spams[target_id]={
     "stage":"active",
     "chat":chat_id,
     "count":sess["count"],
     "emoji":text
    }
    uid=str(sender_id)
    gid=str(chat_id)
    points[uid][gid]["points"]-=sess["count"]*50000
    save_points(points)
    del sessions[sender_id]
    await event.reply("تم التفعيل")
    return
 except Exception as e:
  await event.reply(f"حدث خطأ: {e}")
