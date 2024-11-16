from typing import Any, Optional

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot import callback_data as Q
from bot.texts import get_button_text as _
from core.models import Course, Place
from utils.types import CourseType, PlaceType


def right_to_left_markup(old_list: list[Any]) -> list[Any]:
    new_list = []
    for i in range(0, len(old_list) // 2):
        new_list.append(old_list[i * 2 + 1])
        new_list.append(old_list[i * 2])

    if len(old_list) % 2 != 0:
        new_list.append(old_list[-1])

    return new_list


class Keyboard:
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        builder = ReplyKeyboardBuilder()
        builder.button(text=_("freshman"))
        builder.button(text=_("courses"))
        builder.button(text=_("places"))
        builder.button(text=_("phones"))
        builder.button(text=_("links"))
        builder.button(text=_("about"))
        builder.adjust(1, 2, 2, 1)
        return builder.as_markup()

    @staticmethod
    def freshman(back: bool = False) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        if back:
            builder.button(text=_("back"), callback_data=Q.Freshman(mode=Q.Freshman.Mode.MENU))
        else:
            builder.button(text=_("freshman_register"), callback_data=Q.Freshman(mode=Q.Freshman.Mode.REGISTER))
            builder.button(text=_("back"), callback_data=Q.MainMenu())
        builder.adjust(1, repeat=True)
        return builder.as_markup()


    @staticmethod
    def place(mode: Optional[str] = None, places: Optional[list[Place]] = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        markup_length = 0
        if mode == "group":
            groups = PlaceType.choices
            markup_length = len(groups)
            for group_id, group_name in right_to_left_markup(groups):
                builder.button(text=_(group_name), callback_data=Q.Group(group=group_id))
            builder.button(text=_("back"), callback_data=Q.MainMenu())
        elif mode == "location" and places is not None:
            markup_length = len(places)
            for place in right_to_left_markup(places):
                builder.button(
                    text=place.name,
                    callback_data=Q.Location(latitude=place.latitude, longitude=place.longitude),
                )
            builder.button(text=_("back"), callback_data=Q.Place())

        if markup_length % 2:
            builder.adjust(*[2 for __ in range(markup_length // 2)] + [1, 1])
        else:
            builder.adjust(2)

        return builder.as_markup()
