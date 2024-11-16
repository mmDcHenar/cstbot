from aiogram import Router
from aiogram.types import Message

from bot.keyboards import Keyboard as K
from bot.texts import get_message_text as _

router = Router(name="unknown_command")


@router.message()
async def unknown_command(event: Message) -> Message:
    return await event.answer(_("unknown_command"), reply_markup=K.main_menu())
