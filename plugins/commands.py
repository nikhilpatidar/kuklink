import os
import requests
import asyncio
from presets import Presets
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import Config
from database import BotDatabase

db = BotDatabase('database.db')

VALID_URL = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"

DEFAULT_TOKEN = "0fcf63d87175a2b98663b4ff2b9fe3d979dc7c7b"

# can be used to verify link without https/http/www
# VALID_URL = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"

@Client.on_message(filters.private & filters.command('start'))
async def start(bot, msg):
    user_id = msg.from_user.id
    user_name = '@' + msg.from_user.username if msg.from_user.username else msg.from_user.first_name or 'anonymous'
    db.add_user(user_id, user_name)
    await msg.reply_text(
        Presets.START.format(msg.from_user.mention()),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Presets.buttons)
        )


@Client.on_message(filters.private & filters.command('link'))
async def link(bot, msg):
    user_id = msg.from_user.id
    if len(msg.command) < 2:
        await msg.reply_text('🔗 Use this command to link your API token : <code>/link API_TOKEN</code>')
        return
    query = msg.text.split(' ',maxsplit=1)[1]
    api_call = f"https://kuklink.cf/api?api={query}&url=https://example.com"
    response = requests.get(api_call).json()
    if response['status'].lower() == 'success':
        await msg.reply_text("✅ <b>Success!</b> connected your account. Now send any link you want to shorten.")
        db.add_api_key(user_id, query)
    else:
        await msg.reply_text("❌ Wrong API token! Get your token from https://kuklink.net/member/tools/api", disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command('unlink'))
async def unlink(bot, msg):
    user_id = msg.from_user.id
    db.delete_api_key(user_id)
    await msg.reply_text("✅ Unlinked your account successfully!")


@Client.on_message(filters.private & filters.regex(VALID_URL))
async def short_link(bot, msg):
    user_id = msg.from_user.id
    long_url = msg.text
    try:
        api_key = db.get_api_key(user_id)
        url = f"https://kuklink.net/api?api={api_key[0]}&url={long_url}"
        response = requests.get(url).json()
        short_link = response['shortenedUrl']
        message = f"✅ Your short link : <code>{short_link}</code>\nYou can <b>manage all links</b> here : https://kuklink.net/member/links "
        await msg.reply_text(message, disable_web_page_preview=True)
    except:
        url = f"https://kuklink.net/api?api={DEFAULT_TOKEN}&url={long_url}"
        response = requests.get(url).json()
        short_link = response['shortenedUrl']
        message = f"Your short link : <code>{short_link}</code>\n\n❗️You have not linked your account yet. Link your account and start earning."
        await msg.reply_text(message)


@Client.on_message(filters.private & ~filters.command(["start","link","unlink"]))
async def unknown_command(bot, msg):
    await msg.reply_text("❌ Unknown Command!")


@Client.on_message(filters.private & ~filters.regex(VALID_URL))
async def unknown_message(bot, msg):
    await msg.reply_text("❌ [ERROR] unexpectable input.")
