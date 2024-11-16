from aiogram import Dispatcher, F
from aiogram.enums.chat_type import ChatType

from . import start, main_menu, unknown_command


def setup(dp: Dispatcher):
    dp.message.filter(F.chat.type == ChatType.PRIVATE)
    dp.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

    dp.include_router(start.router)
    dp.include_router(main_menu.router)

    dp.include_router(unknown_command.router)  # this router must be last one
