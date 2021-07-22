from pyrogram.types import InlineKeyboardButton

class Presets(object):
    START = """
Hello <b>{}</b>!

Welcome to kuklink's official bot.
Shorten your links with kuklink and earn upto $20 per 1k views/visits.

🍿 <b>What is kuklink.net ?</b>
Kuklink is a completely free tool where you can create short links, which apart from being free, you get paid! So, now you can make money from home, when managing and protecting your links.
"""
    
    ACCOUNT = """
Hello <b>{}</b>!

user_id : <code>{}</code>
api_token : <code>{}</code>

<b>NOTE</b> : <i>must link your token to start earning.</i>
"""

    EARN  = """
Hey <b>{}</b>, short your links with kuklink and start earning 🤑🤑

🔗 <b>Link Account</b>
<b>1</b> - Create an account on https://kuklink.net

<b>2</b> - Get your api key from <u>kuklink.net/member/tools/api</u>

<b>3</b> - Link your token with this bot using <code>/link API_TOKEN</code>

"""
    buttons = [
            [
                InlineKeyboardButton("🏦 Account", callback_data="account"),
                InlineKeyboardButton("🔑 Link account", callback_data="getapikey")
                ],
            [
                InlineKeyboardButton("🔗 Create kuklink account", url="https://kuklink.net/auth/signup")
                ]
            ]

    home_button = [
            [
                InlineKeyboardButton("🔙 Back to home",callback_data="home")
                ]
            ]
