from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot import callback_data as Q
from bot.texts import get_button_text as _


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
    def back() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=_("back"), callback_data=Q.MainMenu())
        builder.adjust(1, repeat=True)
        return builder.as_markup()
