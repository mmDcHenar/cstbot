from typing import Union

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot import callback_data as Q
from bot.keyboards import Keyboard as K
from bot.texts import get_message_text as _, get_button_text as __
from core.models import Place
from utils.types import PlaceType

router = Router(name="places")


@router.message(F.text == __("places"))
async def places_list(event: Message) -> None:
    await event.answer(_("groups_menu"), reply_markup=K.place(mode="group"))


@router.callback_query(Q.Place.filter())
@router.callback_query(Q.Group.filter())
@router.callback_query(Q.Location.filter())
async def places_menu(event: CallbackQuery, callback_data: Union[Q.Place, Q.Group, Q.Location]) -> None:
    if isinstance(callback_data, Q.Place):
        await event.message.edit_text(_("groups_menu"), reply_markup=K.place(mode="group"))

    elif isinstance(callback_data, Q.Group):
        places = [place async for place in Place.objects.filter(group=callback_data.group).all()]
        text = _("group_places", group=__(PlaceType(callback_data.group).label))
        await event.message.edit_text(text, reply_markup=K.place(mode="location", places=places))

    elif isinstance(callback_data, Q.Location):
        place = await Place.objects.aget(latitude=callback_data.latitude, longitude=callback_data.longitude)
        if place:
            await event.message.delete()
            await event.message.answer_location(latitude=place.latitude, longitude=place.longitude)
            text = _("place", name=place.name, group=__(PlaceType(place.group).label))
            await event.message.answer(text)
            await event.message.send_copy(chat_id=event.from_user.id)
