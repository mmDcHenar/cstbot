from dotenv import load_dotenv
from decouple import config

load_dotenv()

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=str, default="")
BASE_URL = config("BASE_URL", cast=str, default="https://example.com").strip("/")

BOT_TOKEN = config("BOT_TOKEN", cast=str, default="")
BOT_PROXY = config("BOT_PROXY", cast=str, default="") or None
