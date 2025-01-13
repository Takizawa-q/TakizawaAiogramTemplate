from aiogram.filters import BaseFilter
from typing import Any, Awaitable, Callable, Dict
from config import config
from aiogram.types import Message

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        if str(message.from_user.id) in config.tgbot.admins:
            return True
        