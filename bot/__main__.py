import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv

import database.config
from bot.phrases_interpreter import read_file, read_placeholder_file
from bot.routers.command_router import command_router
from bot.states import States
from database.dtos import NewSubscriptionDto, SubscriptionDto, UserDto
from database.repositories import SubscriptionRepository, UserRepository

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'))
dispatcher = Dispatcher()

user_repository = UserRepository(session_maker=database.config.session_maker)
subscription_repository = SubscriptionRepository(session_maker=database.config.session_maker)


async def main():
    dispatcher.include_router(command_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


@dispatcher.message(StateFilter(States.registration_start))
async def register(message: Message, state: FSMContext) -> None:
    subscription: SubscriptionDto = subscription_repository.create(NewSubscriptionDto(description='default', price=0.0))

    user_repository.create(UserDto(user_id=message.from_user.id,
                                   subscription_id=subscription.subscription_id,
                                   language='rus',
                                   registration_date=datetime.now(),
                                   main_name=message.text,
                                   username=message.from_user.username,
                                   balance=0.0,
                                   payments_history=[],
                                   activities=[]))

    await bot.send_message(message.chat.id,
                           await read_placeholder_file('after_name.txt', message.from_user.id) + '\n' + read_file('help.txt'))
    await state.clear()


@dispatcher.message(StateFilter(States.change_name_start))
async def change_name(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')
    user.main_name = message.text
    user_repository.update(message.from_user.id, user)

    await bot.send_message(message.chat.id,
                           await read_placeholder_file('rename_success.txt', message.from_user.id))
    await state.clear()


@dispatcher.message(Command('start'))
async def send_welcome(message: Message, state: FSMContext) -> None:
    if not user_repository.get_by_id(message.from_user.id):
        await message.answer(read_file('first_greeting.txt'))
        await state.set_state(States.registration_start)
    else:
        await message.answer(await read_placeholder_file('again_greeting.txt', message.from_user.id))


asyncio.run(main())
