from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class Registration(StatesGroup):
    message_to_delete = State()
    referal_id = State()
    phone = State()
    mail = State()