from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    registration_start = State()
    change_name_start = State()
    enhance_start_x2 = State()
    enhance_start_x4 = State()
    enhance_start_x8 = State()
    tmp = State()
