from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from asyncio import WindowsSelectorEventLoopPolicy
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import config
from app.db.base import Base
from app.db.engine import create_async_engine, get_session_maker, create_db
from app.middlewares.register_user import RegisterUser
from app.misc.bot_commands import set_bot_commands
import sys
import app
import asyncio


def get_storage():
    if config.redis.use_redis:
        return RedisStorage.from_url(
            f"redis://{config.redis.password}@{config.redis.host}:{config.redis.port}/db",
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()

def register_middlewares(dp: Dispatcher):
    dp.message.middleware(RegisterUser())

def register_routers(dp: Dispatcher):
    dp.include_router(app.handlers.user.prepare_router())
    dp.include_router(app.handlers.admin.prepare_router())

async def on_startup(bot: Bot, admin_ids: list[int]):
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id,
                                   "Hello, if you this, then you're admin!\n<b>/admin</b> - to see admin menu"  )
            await asyncio.sleep(0.05)
        except Exception:
            pass    
            
async def start_db():
    async_engine = await create_async_engine(url=config.db.url)
    session_maker = await get_session_maker(async_engine)
    await create_db(async_engine, Base.metadata)            
    return session_maker
            
async def on_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(app.schedules.send_message_to_channel, "interval", seconds=20, args=[bot])
    scheduler.start()

async def main():
    storage = get_storage()
    bot = Bot(config.tgbot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    session_maker = await start_db()
    
    
    register_routers(dp)
    register_middlewares(dp)
    
    await on_scheduler(bot)
    await on_startup(bot, config.tgbot.admins)
    await set_bot_commands(bot)
    
    await dp.start_polling(bot, session_maker=session_maker) 
       

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass