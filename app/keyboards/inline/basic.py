from app.keyboards.inline.constructor import create_inline_keyboard
from aiogram.utils.keyboard import KeyboardBuilder
class BasicButtons():
    @staticmethod
    def back() -> KeyboardBuilder:
        schema = [1]
        btns = [["🔙 Назад", "back_main"]]
        print("YES")
        return create_inline_keyboard(buttons=btns,
                                      schema=schema)