import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import BOT_TOKEN, BOT_PROXY
from . import handlers, middlewares


def setup():
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        stream=sys.stdout
    )

    dp = Dispatcher()

    middlewares.setup(dp)
    handlers.setup(dp)

    bot = Bot(
        token=BOT_TOKEN,
        session=AiohttpSession(proxy=BOT_PROXY),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    loop = asyncio.new_event_loop()

    # check if connected
    me = loop.run_until_complete(bot.get_me(request_timeout=5))
    logging.info(f"Running on <{me.full_name}>...")

    loop.run_until_complete(dp.start_polling(bot))
