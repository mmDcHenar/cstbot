from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix="main_menu"):
    pass


class Freshman(CallbackData, prefix="freshman"):
    class Mode(str, Enum):
        MENU = "menu"
        REGISTER = "register"

    mode: Mode = "menu"


class Place(CallbackData, prefix="place"):
    pass


class Group(CallbackData, prefix="place"):
    group: int


class Location(CallbackData, prefix="place"):
    latitude: float
    longitude: float
