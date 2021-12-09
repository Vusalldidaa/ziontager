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

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**FlackTagger Bot**, Qurup və ya kanaldaki istifadəçiləri tağ edə bilər ★\nDaha çox məlumat üçün **/help**'ə klikləyin.",
                    buttons=(
                      [Button.url('➕ Qurupa Əlavə Et ➕', 'https://t.me/flacktaggerbot?startgroup=a'),
                      InlineKeyboardButton.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url('👨‍💻 Owner', 'https://t.me/Eyoydu')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Loungetagger bot'un Yardım Menüsü**\n\nKomut: /all \n  Bu komutu, başkalarına bahsetmek istediğiniz metinle birlikte kullanabilirsiniz. \n`Örnek: /all Günaydın!`  \nBu komutu yanıt olarak kullanabilirsiniz. herhangi bir mesaj Bot, yanıtlanan iletiye kullanıcıları etiketleyecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('➕ Qurupa Əlavə Et ➕', 'https://t.me/flacktaggerbot?startgroup=a'),
                      Button.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url(' Yeniliklər 📲', 'https://t.me/FlackResmi'),
                      Button.url('👨‍💻 Owner', 'https://t.me/Eyoydu')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Tağ edmə prosesin ancağ Yönəticilər başlada bilər!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Tağ edmə prosesin ancağ Yönəticilər başlada bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver!__")
  else:
    return await event.respond("__Bir mesaja yanıt verin və ya istifadəçiləri çağırmağ istədiyiniz mətini yazın__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ prosesi uğurlu bir vəzyətdə dayandırldı ✅")
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
        await event.respond("Tağ prosesi uğurlu bir vəzyətdə dayandırldı ✅")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Flack Tagger BoT işləyir 🚀 @FlackResmi kanalına qatılarağ Yeniliklərdən xəbərdar ola bilərsiz <<")
client.run_until_disconnected()
