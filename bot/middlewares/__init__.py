from aiogram import Dispatcher

from .user import DBUserMiddleware


def setup(dp: Dispatcher):
    dp.message.middleware(DBUserMiddleware())
    dp.callback_query.middleware(DBUserMiddleware())
