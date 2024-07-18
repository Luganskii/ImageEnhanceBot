import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from dotenv import load_dotenv

import database.config
from bot.phrases_interpreter import read_file, read_placeholder_file
from database.dtos import NewSubscriptionDto, SubscriptionDto, UserDto
from database.repositories import SubscriptionRepository, UserRepository

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher()

router = Router()

user_repository = UserRepository(session_maker=database.config.session_maker)
subscription_repository = SubscriptionRepository(session_maker=database.config.session_maker)


class States(StatesGroup):
    registration_start = State()
    registration_end = State()
    tmp = State()


async def main():
    await dispatcher.start_polling(bot)
    dispatcher.include_router(router)


@dispatcher.message(StateFilter(States.registration_start))
async def register(message: Message, state: FSMContext) -> None:
    # await bot.delete_message(message.chat.id, message.message_id - 2)
    subscription: SubscriptionDto = subscription_repository.create(NewSubscriptionDto(description='default', price=0.0))

    user_repository.create(UserDto(user_id=message.from_user.id,
                                   subscription_id=subscription.subscription_id,
                                   language='rus',
                                   registration_date=datetime.now(),
                                   main_name=message.text,
                                   username=message.from_user.username))
    await bot.send_message(message.chat.id,
                           await read_placeholder_file('after_name.txt', message.from_user.id) + '\n' + read_file('help.txt'))
    await state.clear()


@dispatcher.message(Command('start'))
async def send_welcome(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('greeting.txt'))
    await state.set_state(States.registration_start)


#
#
# @bot.message_handler(commands=['help'])
# def send_help(message: Message):
#     bot.send_message(message.chat.id, read_file("help.txt"))


asyncio.run(main())
