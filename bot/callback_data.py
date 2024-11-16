from aiogram.filters.callback_data import CallbackData


class MainMenu(CallbackData, prefix="main_menu"):
    pass


class Freshman(CallbackData, prefix="freshman"):
    class Mode(str, Enum):
        MENU = "menu"
        REGISTER = "register"

    mode: Mode = "menu"