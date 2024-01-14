
from typing import Any, Sequence, TypeVar, Literal
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType

class ReplyKeyboardConstructor():
    
    available_properities = [
        "text",
        "request_contact",
        "request_location",
        "request_poll",
        "request_user",
        "request_chat",
        "web_app",
    ]
    
    def __new__(self, buttons: Sequence[str | list[str, str]],
                  schema: Sequence[int]):
        """
        Attributes:
        - buttons: acceptable values for second parameter in dict[str, str]:
            text, request_contact, request_location, request_poll, request_user, request_chat, web_app
        - schema (Sequence[int | str])
        """
        self.buttons = buttons
        self.schema = schema
        builder = ReplyKeyboardBuilder()
        
        for button in self.buttons:
            action: bool = False
            data: dict[str, str | bool] = {}
            
            if isinstance(button, str):
                data["text"] = button
            else:
                print(button, "123")
                if len(button) != 2:
                    raise ValueError("len of list must be == 2")
                arg_name, arg_value = button[0], button[1]
                
                if arg_value not in ReplyKeyboardConstructor.available_properities:
                    raise KeyError(f"action in button must be in list: {ReplyKeyboardConstructor.available_properities}")
                else:
                    data["text"] = arg_name
                    data[arg_value] = True
            print(data)
            builder.add(KeyboardButton(**data))

        builder.adjust(*self.schema)
        return builder.as_markup(resize_keyboard=True)
    
#   b = ReplyKeyboardConstructor([["Привет", "reque t   _contact"],
#                                 "Хватит",
#                                 "Меня убивать"],
#                             [2, 1])
# print(b