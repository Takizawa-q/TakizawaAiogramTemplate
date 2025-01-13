from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from app.handlers.states import AdminMailing
from app.keyboards.inline.constructor import InlineButton, InlineKeyboardConstructor
from app.db.models import user as db
import asyncio


async def start(msg: Message, state: FSMContext):
    buttons = InlineKeyboardConstructor(buttons=[
        InlineButton("📋 Статистика", callback_data="admin_back_from_statistics"),
        InlineButton("📤 Рассылка Пользователям", callback_data="admin_catch_mailing_message"),
        InlineButton("❌ Закрыть")
    ], schema=[1, 1, 1])
    await msg.answer("<b>Admin Menu</b>", reply_markup=buttons)
    await state.clear()

async def statistics(call: CallbackQuery, state: FSMContext, session_maker):
    count_users = await db.get_count_users(session_maker=session_maker)
    text = f"<b>Количество пользователей бота: <code>{count_users.all}</code></b>\n\n" \
           f"За день: <code>{count_users.day}</code>\n" \
           f"За неделю: <code>{count_users.week}</code>\n" \
           f"За месяц: <code>{count_users.month}</code>"
    btn = InlineKeyboardConstructor(buttons=[InlineButton("🔙 Назад", callback_data="admin_back_from_statistics")],
                                    schema=[1])
    await call.message.answer(text, reply_markup=btn)

async def mailing_menu(call: CallbackQuery | Message, state: FSMContext, bot: Bot):
    buttons = InlineKeyboardConstructor(buttons=[InlineButton("✍️ Изменить текст", callback_data="admin_catch_text"),
                                                InlineButton("📷 Добавить фото", callback_data="admin_catch_photo"),
                                                InlineButton("📤 Отправить рассылку", callback_data="admin_finish_mailing")],
                                        schema=[1, 1, 1])
    data = await state.get_data()
    try:
        text = data["text"]
    except Exception:
        text = "Нет"
    if isinstance(call, CallbackQuery):
        message = call.message
        mailing_menu = await message.edit_text(f"Текст: Нет",
                                reply_markup=buttons)
        mailing_menu_id = mailing_menu.message_id
        await state.update_data(mailing_menu_id=mailing_menu_id)
    else:
        message = call
        mailing_menu_id = data["mailing_menu_id"]
        if "photo_id" in data:
            
            photo_id = data["photo_id"]
            await message.answer_photo(photo=photo_id,
                                       caption=text,
                                        message_id=mailing_menu_id,
                                        reply_markup=buttons)
        else:
            await bot.edit_message_text(text=f"Текст:\n{text}",
                                    chat_id=message.from_user.id,
                                    message_id=mailing_menu_id,
                                    reply_markup=buttons)
            
    
async def catch_text(call: CallbackQuery, state: FSMContext):
    message = await call.message.answer("Пришлите текст:")
    mailing_delete_id = message.message_id
    await state.update_data(mailing_delete_id=mailing_delete_id)
    await state.set_state(AdminMailing.text)
    
async def edit_text(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    mailing_delete_id = data["mailing_delete_id"]
    for msg_id in [message.message_id, mailing_delete_id]:
        await bot.delete_message(chat_id=message.from_user.id,
                                message_id=msg_id)
    await state.update_data(text=message.text)
    await mailing_menu(call=message, state=state, bot=bot)

async def catch_photo(call: CallbackQuery, state: FSMContext):
    message = await call.message.answer("Пришлите фото:")
    photo_delete_id = message.message_id
    await state.set_state(AdminMailing.photo)
    await state.update_data(photo_delete_id=photo_delete_id)
    
async def edit_photo(message: Message, bot: Bot, state: FSMContext):
    
    await state.update_data(photo_id=message.photo[-1].file_id)
    await mailing_menu(message, state, bot)

async def finish_mail(call: CallbackQuery, bot: Bot, session_maker, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    users: list[db.UserDTO] = await db.get_all_users(session_maker)
    good, error = 0, 0
    for user in users:
        try:
            if "photo_id" in data:
                await bot.send_photo(chat_id=user.user_id,
                                    photo=data["photo_id"],
                                    caption=text)
            else:
                await bot.send_message(chat_id=user.user_id,
                                    text=text)
            good += 1
        except Exception as e:
            print(e)
            error += 1
        await asyncio.sleep(0.5)
    await call.message.answer(f"✅ <b>Рассылка закончена!</b>\n\nУдачно отправлено: <code>{good}</code>\nНе отправилось: <code>{error}</code>")
        