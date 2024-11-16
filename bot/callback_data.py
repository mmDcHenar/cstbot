from enum import Enum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix="main_menu"):
    pass


class Freshman(CallbackData, prefix="freshman"):
    class Mode(str, Enum):
        MENU = "menu"
        REGISTER = "register"

    mode: Mode = "menu"


class CoursesFilter(CallbackData, prefix="courses"):
    filter_by: Optional[str] = None
    value: Optional[int] = None


class Course(CallbackData, prefix="course"):
    filter_by: str
    id: int


class Place(CallbackData, prefix="place"):
    pass


class Group(CallbackData, prefix="place"):
    group: int


class Location(CallbackData, prefix="place"):
    latitude: float
    longitude: float
