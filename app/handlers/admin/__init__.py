from aiogram import Router, F
from app.filters.admin import AdminFilter
from app.handlers.states import AdminMailing
from . import admin

def prepare_router() -> Router:
    admin_router = Router()
    admin_router.message.register(admin.start, F.text=="/admin", AdminFilter())
    # admin_router.callback_query.register(admin.statistics, F.data=="admin_back_from_statistics", AdminFilter())
    
    admin_router.callback_query.register(admin.mailing_menu, F.data=="admin_catch_mailing_message", AdminFilter())
    admin_router.callback_query.register(admin.catch_text, F.data=="admin_catch_text", AdminFilter())
    admin_router.message.register(admin.edit_text, AdminMailing.text, AdminFilter())
    
    admin_router.callback_query.register(admin.catch_photo, F.data=="admin_catch_photo", AdminFilter())
    admin_router.message.register(admin.edit_photo, AdminMailing.photo, AdminFilter())
    
    admin_router.callback_query.register(admin.finish_mail, F.data=="admin_finish_mailing", AdminFilter())
    return admin_router

