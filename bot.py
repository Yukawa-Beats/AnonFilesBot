#    Copyright (C) 2021 - Avishkar Patil | @AvishkarPatil


import os
import sys
import time
import logging
import pyrogram
import aiohttp
import asyncio
import requests
import aiofiles
from random import randint
from progress import progress
from config import Config
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

DOWNLOAD = "./"

# vars
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN

   
bot = Client(
    "AnonFilesBot",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


START_TEXT = """
__Hello__ {} I am **YB URL GENERATOR BOT** 😎 \n\n__I CAN CONVERT TELEGRAM FILES TO DIRECT LINK__\n\n__Maintained by__ :<a href='https://t.me/ybdemochannel'>YUKAWA BEATS</a>
"""
HELP_TEXT = """
ഓ അവൻ ഹെല്പ് ചോതിച്ചു വന്നേക്കുന്നു😏..എന്തായാലും വന്നതല്ലേ പറഞ്ഞു തരാം..🤨താഴോട്ട് നോക്ക്👇\n\n**YB URL GENERATOR BOT Help**👇\n\n__SEND ME ANY TELEGRAM MEDIA FILE, I WILL GIVE YOU DIRECT DOWNLOAD LINK__\n\n__Maintained by__ :<a href='https://t.me/ybdemochannel'>YUKAWA BEATS</a>
"""
ABOUT_TEXT = """
- **Bot :** `YB URL GENERATOR BOT`
- **Creator :** [YUKAWA BEATS](https://telegram.me/ybdemochannel)
- **Source :** [Click here](https://github.com/Yukawa-Beats/AnonFilesBot)
- **Language :** [Python3](https://python.org)
- **Server :** [Heroku](https://heroku.com)

മാസ്റ്റർ ബ്രെയിൻ😎😎 :<a href='https://t.me/ybdemochannel'>YUKAWA BEATS</a>
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )


@bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()
        
        
@bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

      
@bot.on_message(filters.media & filters.private)
async def upload(client, message):
    if Config.UPDATES_CHANNEL is not None:
        try:
            user = await client.get_chat_member(Config.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.chat.id,
                    text="സോറി മോനെ..നീ ബാൻ ആയി കേട്ടോ🤭😂",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="എന്റെ ചാനലിൽ ജോയിൻ ചെയ്യടാ...എന്നാലേ എന്നെക്കൊണ്ട് എന്തേലും നടക്കൂ..കേട്ടോ 🏃‍♂**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Join Channel", url=f"https://t.me/{Config.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.chat.id,
                text="എന്തോ പ്രശ്നം ഉണ്ടല്ലോ ചങ്ങായി",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    m = await message.reply("നിങ്ങളുടെ ഫയൽസ് എന്റെ സെർവേറിലേക്ക് ഡൌൺലോഡ് ചെയ്യുകയാണ് ദയവായി കാത്തിരിക്കൂ.. 😈")
    now = time.time()
    sed = await bot.download_media(
                message, DOWNLOAD,
          progress=progress,
          progress_args=(
            "അപ്‌ലോഡ് പ്രോസസ് തൊടങ്ങി മോനെ..ഇനി എന്റെ മാജിക് കണ്ടോ..ഓം ഹ്രീം കുട്ടിച്ചാത്താ👹\nനിന്റെ ഫയല്സിന്റെ സൈസ് നു അനുസരിച്ചുള്ള സമയം എടുക്കും കേട്ടോ..🤧 \n\nഏകദേശം:** ", 
            m,
            now
            )
        )
    try:
        files = {'file': open(sed, 'rb')}
        await m.edit("എന്റെ സെർവേറിലേക്ക് ഫയൽസ് അപ്‌ലോഡ് ആകുന്നുണ്ട്..ദിപ്പൊ ശരിയാക്കിത്തരാം..🤒")
        callapi = requests.post("https://api.anonfiles.com/upload", files=files)
        text = callapi.json()
        output = f"""
<u>മോനെ ഫയൽ സെറ്റ് ആയിട്ടുണ്ട്..എടുത്തോണ്ട് പൊക്കോ..🤪*/u>

📂 ഫയലിന്റെ പേര്: {text['data']['file']['metadata']['name']}

📦 ഫയലിന്റെ വലിപ്പം: {text['data']['file']['metadata']['size']['readable']}

📥ഇന്നാ ലിങ്ക്👉: `{text['data']['file']['url']['full']}`

🔅മാസ്റ്റർ ബ്രെയിൻ😎😎 :<a href='https://t.me/ybdemochannel'>YUKAWA BEATS</a>
   ഡൌൺലോഡ് ചെയ്യാൻ താഴെ തൊട് 👇
"""
        btn = InlineKeyboardMarkup(
                                [[InlineKeyboardButton("DOWNLOAD", url=f"{text['data']['file']['url']['full']}")]])
        await m.edit(output, reply_markup=btn)
        os.remove(sed)
    except Exception:
        await m.edit("ഇത് വലിയ സൈസ് ആണ്..ഇത് എന്നെകൊണ്ട് പറ്റും എന്ന് തോന്നുന്നില്ല ഷാജിയെട്ടാ🙏")
        return
      
@bot.on_message(filters.regex(pattern="https://cdn-") & filters.private & ~filters.edited)
async def url(client, message):
    msg = await message.reply("ലിങ്ക് നോക്കട്ടെ👀")
    lenk = message.text
    cap = "മാസ്റ്റർ ബ്രെയിൻ😎😎 :<a href='https://t.me/ybdemochannel'>YUKAWA BEATS</a>"
    thumb = "./thumb.jpg"
    try:
         await msg.edit("പേടിക്കണ്ട മോനെ..വലിയ ഫയല്സിന് ടൈം എടുക്കും..കെട്ടോ😼")
         filename = await download(lenk)
         await msg.edit("ടെലിഗ്രാമിലേക്ക് ഫയൽ അപ്‌ലോഡ് ചെയ്യുന്നുണ്ട്...")
         await message.reply_document(filename, caption=cap, thumb=thumb)
         await msg.delete()
         os.remove(filename)
    except Exception:
        await msg.edit("ഇത് വലിയ സൈസ് ആണ്..ഇത് എന്നെകൊണ്ട് പറ്റും എന്ന് തോന്നുന്നില്ല ഷാജിയെട്ടാ🙏")
        
async def download(url):
    ext = url.split(".")[-1]
    filename = str(randint(1000, 9999)) + "." + ext
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return filename
        
        
bot.start()
print("YB URL GENERATOR BOT Is Started")
idle()
