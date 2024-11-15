from aiogram import Dispatcher, F
from aiogram.enums.chat_type import ChatType

from . import start


def setup(dp: Dispatcher):
    dp.message.filter(F.chat.type == ChatType.PRIVATE)
    dp.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

    dp.include_router(start.router)
