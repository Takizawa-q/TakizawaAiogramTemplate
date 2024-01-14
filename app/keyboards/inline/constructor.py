from typing import Sequence
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def create_inline_keyboard(buttons: list[Sequence[str]], schema: Sequence[int],
                           request_contact: bool = False) -> ReplyKeyboardBuilder:
    if not isinstance(buttons, list):
        return TypeError("Wrong button type. It must be str or list")
    builder = InlineKeyboardBuilder()
    for button_text, button_cb in buttons:
        builder.add(InlineKeyboardButton(text=button_text,
                                         request_contact=request_contact,
                                        callback_data=button_cb))
    builder.adjust(*schema)
    return builder