from dataclasses import dataclass
from aiogram.types import CallbackQuery, Message, TelegramObject

@dataclass
class User():
    user_id: int
    username: str
    fullname: str
    
async def get_user_from_event(event: CallbackQuery | Message) -> User:
    return User(
        user_id=event.from_user.id,
        username=event.from_user.username,
        fullname=event.from_user.full_name
                )