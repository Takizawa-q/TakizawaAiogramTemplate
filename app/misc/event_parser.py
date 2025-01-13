from dataclasses import dataclass
from aiogram.types import CallbackQuery, Message, TelegramObject
from app.db.models.user import User
    
def get_user_from_event(event: CallbackQuery | Message) -> User:

    return User(
        user_id=event.from_user.id,
        username=event.from_user.username,
        full_name=event.from_user.full_name
                )