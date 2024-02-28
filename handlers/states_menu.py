from aiogram.filters.state import State, StatesGroup

class States(StatesGroup):
    my_state = State()
    none_state = State()