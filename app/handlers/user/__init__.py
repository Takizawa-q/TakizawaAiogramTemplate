from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters import CommandStart
from enum import IntEnum
from . import start

def prepare_router() -> Router:
    user_router = Router()
    user_router.message.register(start.start, CommandStart())
    return user_router

