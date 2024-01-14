from aiogram import types
from aiogram import Bot
from app.keyboards.inline.basic import BasicButtons
from aiogram.utils.deep_linking import create_deep_link, create_start_link, create_telegram_link
import app.db
from app.misc.redis_connection import redis




async def generate_main_text(call: types.CallbackQuery,
                        bot: Bot, 
                        referal_username: str,
                        referal_id: str | int,
                        refered_by_me_count: str | int,
                        refered_by_me_count_month: str | int):
    data = await create_start_link(bot, str(call.from_user.id), encode=False)
    return f"""<b>Тебя пригласил:</b> {"@" + referal_username if referal_username else "никто"} 🔥

💰 <b>Баланс:</b> <code>xxx</code>

🎯 <b>Твоя реферальная ссылка:</b> <code>{data}</code>

🤩 <b>Приглашено тобой:</b>
├<b>За текущий месяц:</b> <code>{refered_by_me_count_month}</code>
└<b>Всего:</b> <code>{refered_by_me_count}</code>

👉 <b>Приглашено твоими партнерами</b>
├<b>За текущий месяц:</b> <code>0</code>
└<b>Всего:</b> <code>0</code>

💰 <b>Заработано рублей:</b> <code>0</code>
├<b>За сегодня:</b> <code>0</code>
├<b>За личные приглашения:</b> <code>0</code>
└<b>От приглашений партнеров:</b> <code>0</code>
"""

async def profile(call: types.CallbackQuery, bot: Bot):
    back_button = BasicButtons().back()

    
    user_id = call.from_user.id

    referal_id = await app.db.models.user.get_my_referal_id(user_id=user_id)
    refered_by_me_count = await app.db.models.user.get_my_referals_count(user_id=user_id)
    refered_by_me_count_month = await app.db.models.user.get_my_referals_count_month(user_id=user_id)
    referal_username = await redis.get(name=f"{referal_id}")
    print(refered_by_me_count_month)
    text = await generate_main_text(call,
                                    bot=bot,
                                    referal_username=referal_username,
                                    referal_id=referal_id,
                                    refered_by_me_count=refered_by_me_count,
                                    refered_by_me_count_month=refered_by_me_count_month)
    
    await call.message.edit_text(text=text,
                              reply_markup=back_button.as_markup())