from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from app.states.registration import Registration
from app.misc.event_parser import get_user_from_event
from app import db
import asyncio
from app.keyboards.reply.constructor import ReplyKeyboardConstructor
from app.handlers.user.start import start


async def start_registration(message: types.Message, state: FSMContext, referal_id: int):
    await state.update_data(name=message.text)
    await state.update_data(referal_id=referal_id)
    msg = await message.answer("\n".join(["Привет 👋",
        "\nСмотрю вы у нас в первый раз, давайте пройдем небольшую регистрацию.",
        "Напишите ваш e-mail 📥 в чат.",
        "<b>Чтобы мы всегда могли быть с вами на связи!</b>"]))
    await message.delete()
    await state.update_data(message_to_delete=[msg.message_id, message.chat.id])
    await state.set_state(Registration.mail)

async def phone(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id, chat_id = data["message_to_delete"][0], data["message_to_delete"][1]
    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)
    kb = ReplyKeyboardConstructor([
        ["✅ Оставить номер", "request_contact"],
        "⚠️ Не оставлять номер"],
                                    
        schema=[1, 1]
        )
    await message.delete()
    msg = await message.answer("\n".join(["По желанию, можно оставить свой номер телефона ☎️",
                                "Передавая нам свой номер телефона, мы обязуемся не раскрывать ваши данные третьим лицам и не распространять персональные данные",
                                "\n<b>В соответствии с: 152-ФЗ \"О персональных данных\"</b>"],),
                            reply_markup=kb)
    await state.update_data(message_to_delete=[msg.message_id, message.chat.id])
    await state.set_state(Registration.phone)
    await state.update_data(mail=message.text)
    

async def finish_registration(message: types.Message | types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    message_id, chat_id = data["message_to_delete"][0], data["message_to_delete"][1]
    await bot.delete_message(chat_id=chat_id,
                             message_id=message_id)
    if isinstance(message, types.CallbackQuery):
        message = message.message
    state_data = await state.get_data()
    await message.delete()
    user = await get_user_from_event(message)
    try:
        phone_number = message.contact.phone_number
    except AttributeError:
        phone_number = None
    email = state_data["mail"]
    referal_id = state_data["referal_id"]
    await state.clear()
    msg = await message.answer("\n".join([
        "Вы зарегестрированы ✅",
        "\n<b><i>Добро пожаловать!</i></b> "
    ]))
    await db.models.user.register_user(
                user_id=user.user_id,
                username=user.username,
                fullname=user.fullname,
                email=email,
                phone_number=phone_number,
                referal_id=referal_id
                
            )
    await asyncio.sleep(4)
    await msg.delete()
    
    await start(msg, state)
    