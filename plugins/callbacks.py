from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from presets import Presets
from database import BotDatabase

db = BotDatabase('database.db')

getapikey_filter = filters.create(lambda _, __, query: query.data.lower() == "getapikey")
account_filter = filters.create(lambda _, __, query: query.data.lower() == "account")
home_filter = filters.create(lambda _, __, query: query.data.
lower() == "home")

@Client.on_callback_query(account_filter)
async def _account(bot, callback_query):
    chat_id = callback_query.from_user.id
    user = callback_query.from_user.mention()
    message_id = callback_query.message.message_id
    try:
        api_key = db.get_api_key(chat_id)[0]
    except:
        api_key = "❌ No API token linked."
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Presets.ACCOUNT.format(user, chat_id, api_key),
        reply_markup=InlineKeyboardMarkup(Presets.home_button),
    )


@Client.on_callback_query(getapikey_filter)
async def _apikey(bot, callback_query):
    chat_id = callback_query.from_user.id
    user = callback_query.from_user.mention()
    message_id = callback_query.message.message_id
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Presets.EARN.format(user),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Presets.home_button),
    )

@Client.on_callback_query(home_filter)
async def _home(bot, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=Presets.START.format(callback_query.from_user.mention()),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Presets.buttons)
        )
