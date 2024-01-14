from aiogram.filters import BaseFilter
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message

class ValidEmailFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        # Если entities вообще нет, вернётся None,
        # в этом случае считаем, что это пустой список
        
        if all([symb in message.text for symb in ["@", "."]]):
            return True
        else:
            await message.answer("⚠️ Некоректный формат e-mail."
                             "\nУбедитесь, что в почте есть <code>@</code> и <code>.</code>")
        