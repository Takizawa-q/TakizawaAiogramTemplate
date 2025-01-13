from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker
from app.db.models.user import get_all_users, add_user, UserDTO
from app.misc.event_parser import get_user_from_event

# async def start(message: Message, session_maker: sessionmaker):
#     current_user = get_user_from_event(event=message)
#     users: list[UserDTO] = await get_all_users(session_maker)
#     user_ids: list[int] = [user.user_id for user in users]
            
#     await message.answer("you wrote: /start")

async def start(message: Message, session_maker: sessionmaker):
    current_user = get_user_from_event(event=message)
    users: list[UserDTO] = await get_all_users(session_maker)
    user_ids: list[int] = [user.user_id for user in users]
    if message.from_user.id not in user_ids:
        await add_user(current_user, session_maker)
        print("Created: ", current_user)
            
    
    await message.answer("/start")
    