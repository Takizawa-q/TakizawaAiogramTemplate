from aiogram import types, html
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.keyboards.inline.constructor import create_inline_keyboard
from app.keyboards.reply.constructor import ReplyKeyboardConstructor

TEXT = """💡 Это основное меню, и отсюда я готов предоставить тебе всю информацию!

🙏 Наше предложение включает в себя как готовых чат-ботов для традиционного и МЛМ бизнеса, так и обучающие платформы, а также онлайн курсы по созданию чат-ботов и партнерскую программу от сервиса SX_100!

✅ В настоящее время у тебя <b>xxx</b> баллов (рублей)! (Обрати внимание, что они доступны до 23:59 сегодня, и после этого они обнулятся.)

😎 Просто выбери то, что тебя интересует, и я расскажу тебе больше."""

def generate_menu_buttons() -> InlineKeyboardBuilder:
    main_menu_buttons = [
        ["🏆 Мой Профиль", "user_profile"],
        ["💰 Партнерство", "partnership"],
        ["🤖 Наши боты", "my_bots"],
        ["📑 Юридическая информация по боту", "laws_info"]]
    builder = create_inline_keyboard(buttons=main_menu_buttons,
                                     schema=[2, 1, 1])
    return builder
    
async def start(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return
    main_menu_buttons = generate_menu_buttons()
    
    if isinstance(msg, types.Message):
        if msg.text == "/start":
            open_menu_button = ReplyKeyboardConstructor(["🧳 Открыть меню"],
                                            [1])
            await msg.answer(f"Привет, {msg.from_user.full_name}",
                             reply_markup=open_menu_button)
        
        await msg.answer(text=TEXT,
                        reply_markup=main_menu_buttons.as_markup())
        
    if isinstance(msg, types.CallbackQuery):
        call: types.CallbackQuery = msg
        if call.message.text == "/start":
            builder = ReplyKeyboardConstructor(["🧳 Открыть меню"],
                                            [1])
        await call.message.edit_text(text=TEXT,
                        reply_markup=main_menu_buttons.as_markup())

# async def test(msg: types.Message):
#     m = [
#         f'Hello, <a href="tg://user?id={msg.from_user.id}">{html.quote(msg.from_user.full_name)}</a>'
#     ]


#     await msg.answer("\n".join(m), reply_markup=builder.as_markup(resize_keyboard=True))
