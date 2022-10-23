import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):
    TG_BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    APP_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    DB_URL = os.environ.get("DATABASE_URL", "")

    # Group/Channel username of the support chat.
    # SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "@sumit_ptdr")

    # List of admin user ids for special functions(Storing as an array)
    #AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "943097546").split())


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
