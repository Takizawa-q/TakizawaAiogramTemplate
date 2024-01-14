from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import Message
import app
from app.config import config
import asyncio

def get_storage():
    if config.redis.use_redis:
        return RedisStorage.from_url(
            f"redis://{config.redis.password}@{config.redis.host}:{config.redis.port}/db",
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def register_middlewares():
    pass

def register_routers(dp: Dispatcher):
    dp.include_router(app.handlers.user.prepare_router())

async def on_startup(bot: Bot, admin_ids: list[int]):
    print(admin_ids)
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, "hello world!")
            await asyncio.sleep(0.05)
        except Exception:
            pass
            

async def main():
    storage = get_storage()
    
    bot = Bot(config.tgbot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    
    register_routers(dp)
    
    await on_startup(bot, config.tgbot.admins)
    await dp.start_polling(bot)
    
    
    
    

if __name__ == "__main__":
    asyncio.run(main())