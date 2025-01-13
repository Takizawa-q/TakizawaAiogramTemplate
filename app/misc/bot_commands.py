from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
    ]
    
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())