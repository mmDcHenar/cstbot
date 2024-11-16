from typing import Union

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot import callback_data as Q
from bot.keyboards import Keyboard as K
from bot.texts import get_message_text as _, get_button_text as __

router = Router(name="freshman")


@router.message(lambda f: f.text == __("freshman"))
@router.callback_query(Q.Freshman.filter(F.mode == Q.Freshman.Mode.MENU))
async def freshman_menu(event: Union[CallbackQuery, Message]) -> None:
    if isinstance(event, Message):
        await event.answer(_("freshman_menu"), reply_markup=K.freshman())
    else:
        await event.message.edit_text(_("freshman_menu"), reply_markup=K.freshman())


@router.callback_query(Q.Freshman.filter(F.mode == Q.Freshman.Mode.REGISTER))
async def freshman_register(event: CallbackQuery) -> None:
    await event.message.edit_text(_("freshman_register"), reply_markup=K.freshman(back=True))
