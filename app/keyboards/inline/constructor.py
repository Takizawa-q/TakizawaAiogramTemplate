from typing import Sequence
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
)
from aiogram.types import (
    InlineKeyboardButton,
    WebAppInfo,
    WebAppData,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    CallbackGame
)
from dataclasses import dataclass
from typing import Optional


@dataclass
class InlineButton():
    text: str
    callback_data: Optional[int] = None
    url: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None


class InlineKeyboardConstructor():
    available_properities = [
        "text",
        "callback_data",
        "url",
        "login_url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
        "pay",
    ]

    def __new__(self, buttons: list[InlineButton],
                schema: Sequence[int]) -> InlineKeyboardMarkup:

        if not isinstance(buttons, list):
            return TypeError("Wrong button type. It must be str or list")
        builder = InlineKeyboardBuilder()

        for button in buttons:
            if not button.callback_data: button.callback_data = "None"
            builder.add(InlineKeyboardButton(
                text=button.text,
                url=button.url,
                callback_data=button.callback_data,
                web_app=button.web_app,
                login_url=button.login_url,
                switch_inline_query=button.switch_inline_query,
                switch_inline_query_current_chat=button.switch_inline_query_current_chat,
                switch_inline_query_chosen_chat=button.switch_inline_query_chosen_chat,
                callback_game=button.callback_game,
                pay=button.pay,
            ))
        builder.adjust(*schema)
        return builder.as_markup()
