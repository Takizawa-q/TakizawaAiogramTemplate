from aiogram.fsm.state import StatesGroup, State

class AdminMailing(StatesGroup):
    text = State()
    photo = State()