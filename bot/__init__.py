import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage, RedisEventIsolation

from . import handlers, middlewares, texts
from config import BOT_TOKEN, BOT_PROXY, REDIS_PORT, REDIS_HOST


def setup():
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        stream=sys.stdout
    )

    texts.manager.load_all_text_from_db()

    storage = RedisStorage.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        key_builder=DefaultKeyBuilder(with_bot_id=True)
    )

    dp = Dispatcher(storage=storage, events_isolation=RedisEventIsolation(storage.redis))

    middlewares.setup(dp)
    handlers.setup(dp)

    bot = Bot(
        token=BOT_TOKEN,
        session=AiohttpSession(proxy=BOT_PROXY),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True)
    )

    loop = asyncio.new_event_loop()

    # check if connected
    me = loop.run_until_complete(bot.get_me(request_timeout=5))
    logging.info(f"Running on <{me.full_name}>...")

    loop.run_until_complete(dp.start_polling(bot))
