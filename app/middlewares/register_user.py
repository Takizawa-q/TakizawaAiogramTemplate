from typing import Any, Awaitable, Callable, Dict
import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


from app.misc.event_parser import get_user_from_event
from app.misc.redis_connection import redis
from app.handlers.user.registration import start_registration
from aiogram.utils.deep_linking import decode_payload

class RegisterUser(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        
        
        user = await get_user_from_event(event)

        if not await redis.get(name=f"{user.user_id}"):
            await redis.set(name=f"{user.user_id}", value=user.username)
            message: Message = event
            split_msg = message.text.split(" ")
            if len(split_msg) >= 2:
                referal_id: int = int(split_msg[1])
            else:
                referal_id = None
            await start_registration(message=event,
                                     state=data['state'],
                                     referal_id=referal_id)
        else:
            return await handler(event, data)
