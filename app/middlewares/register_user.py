from typing import Any, Awaitable, Callable, Dict
import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from config import config
from app.db.models.user import add_user
from app.misc.event_parser import get_user_from_event
from app.misc.redis_connection import redis

class RegisterUser(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user = get_user_from_event(event)
        session_maker = data["session_maker"]
        # if not await redis.get(name=f"if_user_exists: {str(user.user_id)}"):
        #     await add_user(user, session_maker)
        #     await redis.set(name=f"if_user_exists: {str(user.user_id)}", value=1)
        
        
        
        return await handler(event, data)
