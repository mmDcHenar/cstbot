from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def start(event: Message) -> Message:
    return await event.answer("welcome")
