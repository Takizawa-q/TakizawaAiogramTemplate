from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters import CommandStart
from app.states.registration import Registration
from app.filters.text import ValidEmailFilter
from . import start
from . import profile
from . import registration
from . import my_bots

def prepare_router() -> Router:
    user_router = Router()
    
    # user_router.message.register(registration.start_registration)
    
    # user_router.message.register(registration.mail, Registration.name)
    user_router.message.register(registration.phone, Registration.mail, ValidEmailFilter())
    user_router.message.register(registration.finish_registration, Registration.phone)
    user_router.callback_query.register(registration.finish_registration,
                                        Registration.phone,
                                        F.data.in_({"phone_access",
                                                    "phone_deny"}))
    user_router.message.register(start.start, F.text.in_({"🧳 Открыть меню",
                                                         "/start"}))
    user_router.callback_query.register(profile.profile, F.data == "user_profile")
    user_router.callback_query.register(start.start, F.data == "back_main")
    
    user_router.callback_query.register(my_bots.my_bots, F.data.in_({"my_bots",
                                                                     "back_my_bots"}))
    user_router.callback_query.register(my_bots.ready_bots, F.data == "ready_bots")
    user_router.callback_query.register(my_bots.ready_bots_ref, F.data == "ready_bots_ref")
    
    return user_router

