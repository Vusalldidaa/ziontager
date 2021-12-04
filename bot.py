import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/dayan'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Oscar Tag Bot**, Qrupda və ya kanalda demək olar ki, istənilən üzvü qeyd edə bilərəm ★\nƏtraflı məlumat üçün **/help** üzərinə klikləyin.",
                    buttons=(
                      [Button.url('🌟 Meni Bir Gruba Ekle', 'https://t.me/OscarTagBot?startgroup=a'),
                      Button.url('📣 Sohbet Qrupumuz', 'https://t.me/OSCAR_sohbet'),
                      Button.url('🧑‍💻 Sahibim', 'https://t.me/Roxy_Boss')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Oscar Tag botunun Yardım Menyu**\n\nƏmr: /tag \n Bu emri başqalarına söylemek istediyiniz metnle birlikdw istifade ede bilersiniz.  \n`Nümune: /tag sabahınız xeyir!` \nBu emrden cavab olaraq istifade ede bilərsiniz.  istənilən mesaj Bot istifadəçiləri cavablandırılan mesaja tag edecek /dayan- bu emrle prosesi dayandıra bilərsiniz @piramidasohbet Söhbet Kanalımıza gelmeyi unutmayın"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Meni Bir Gruba Ekle', 'https://t.me/OscarTagBot?startgroup=a'),
                       Button.url('📣 Sohbet Qrupumuz', 'https://t.me/OSCAR_sohbet'),
                      Button.url('🧑‍💻 Sahibim', 'https://t.me/Roxy_Boss')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda islede bilersen.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca yöneticiler Herkesden Bahs Ede Biler!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Kohne mesajlar için üyeleri tag edemerem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver!__")
  else:
    return await event.respond("__Bir mesajı yanıtlayın veya başkalarıni tag etmek  ucun mene bir metin verin!__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tag Prosesi Ugurla Dayandirildi❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tag Prosesi Ugurla Dayandirildi ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
emj = ['😇','🥰','😎','🤩','😍','👾','🤡','🥳','😻','😼','😽','💋','👸','🤴','🎅🏻','🤶','🧞‍♀️','🧞','🧞‍♂️','🧜‍♀️','🧜','🧚‍♀️','🧚','👑','💍','🕶','🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼','🐨','🐯','🦁','🐮','🐷','🐽','🐸','🐵','🙈','🙉','🙊','🐒','🐣','🐥','🦅','🐝','🦋','🐞','💐','🌹','🥀','🌺','🌸','🌼','🌻','⭐️','🌟','✨','⚡️','🔥','🌈','☃️','🍫','💅','🐺','🍫','🍕','☕','🧸','🦅','👩‍🦰','🎮','☄️','🌙','🦕','👨🏻‍✈️','🥶','🍿','👀','💀','💟','♥️','💘','💝','💗','💙','💛','🖤','🤑','⚡','😈','🤡','🎊','🔥','😼','💤','✊','👩‍🎨','🧕','🌼','💐','🌹','🥀','🌷','🌺','🌸','🏵️','🌻','🍂','🍁','🌾','🌱','🌿','🍃','☘️','🍀','🌵','🌴','🌳','🌲','🏞️','🌪️','☃️','⛄','❄️','🏔️','🌋','🙋','🤶','👩‍💼','🧓','🧔','💃','🕺','👩‍🦰','🪐','🦄','🐢','🐁','🐤','🐣','🐥','🦉','🐓','🕊️','🦢','🦩','🦈','🐬','🐋','🐳','🐟','🐠','🦚','🐡','🦐','🦞','🦀','🦑','🐙','🦂','🕷️','🕸️','🐜','🦗','🦟','🐝','🐞','🐾','🍓','🍒','🍎','🍉','🍊','🥭','🍍','🍋','🍇','🥝','🍐','🥥','🌶️','🍄','🍔','🧆','🥙','🦞','🍧','🍨','🍦','🥧','🍰','🍮','🎂','🧁','🍭','🍬','🍩','🍺','🍻','🥂','🍾','🍷']

@aykhan(outgoing=True, pattern="^/etag.*")
async def emtag(event):
      if event.fwd_from or FlagContainer.is_active:
          return
      try:
          FlagContainer.is_active = True
  
          sozemj = None
          aykhan4 = event.message.text.split(" ", 1)
          if len(aykhan4) > 1:
              sozemj = aykhan4[1]
  
          chat = await event.get_input_chat()
          await event.delete()
  
          tags = list(map(lambda m: f"[{random.choice(emj)}](tg://user?id={m.id})", await event.client.get_participants(chat)))
          current_pack = []
          async for participant in event.client.iter_participants(chat):
              if not FlagContainer.is_active:
                  break
  
              current_pack.append(participant)
  
              if len(current_pack) == 5: 
                  tags = list(map(lambda m: f"[{random.choice(emj)}](tg://user?id={m.id})", current_pack))
                  current_pack = []
  
                  if sozemj:
                      tags.append(sozemj)
  
                  await event.client.send_message(event.chat_id, " ".join(tags))
                  await asyncio.sleep(0.5) 
      finally:
          FlagContainer.is_active = False

print(">> Bot isdeyir merak eleme 🚀 @Roxy_Boss bilgi alabilersen <<")
client.run_until_disconnected()
