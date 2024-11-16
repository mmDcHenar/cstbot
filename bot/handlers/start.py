from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.texts import get_message_text as _
from bot.keyboards import Keyboard as K

router = Router(name="start")


@router.message(CommandStart())
async def start(event: Message) -> Message:
    return await event.answer(_("welcome", full_name=event.from_user.full_name), reply_markup=K.main_menu())
