from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from bot import callback_data as Q
from bot.keyboards import Keyboard as K
from bot.texts import get_message_text as _, get_button_text as __
from core.models import Link, Phone

router = Router(name="main_menu")


@router.callback_query(Q.MainMenu.filter())
async def main_menu(event: CallbackQuery) -> None:
    try:
        await event.message.delete()
    except TelegramBadRequest:
        pass
    await event.message.answer(_("back_main_menu"), reply_markup=K.main_menu())


@router.message(lambda e: e.text == __("phones"))
async def phones_list(event: Message) -> None:
    phones = [
        _("phone_template", name=phone.name, phone_number=phone.phone_number)
        async for phone in Phone.objects.filter().all()
    ]
    await event.answer(_("phones", phones="\n\n".join(phones)))


@router.message(lambda e: e.text == __("links"))
async def links_list(event: Message) -> Message:
    links = [
        _("link_template", name=link.name, address=link.address)
        async for link in Link.objects.filter().all()
    ]
    return await event.answer(_("links", links="\n\n".join(links)))


@router.message(lambda e: e.text == __("about"))
async def about(event: Message) -> Message:
    return await event.answer(_("about"))
