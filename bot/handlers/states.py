from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    get_login = State()
    get_password = State()