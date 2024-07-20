import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.routers.command_router import command_router
from bot.routers.simple_states_router import simple_states_router

load_dotenv()
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dispatcher = Dispatcher()
    dispatcher.include_routers(command_router, simple_states_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


asyncio.run(main())
