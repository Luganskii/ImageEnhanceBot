from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    registration_start = State()
    change_name_start = State()
    enhance_start = State()
    tmp = State()
