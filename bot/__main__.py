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
    change_name_start = State()
    tmp = State()


async def main():
    await dispatcher.start_polling(bot)
    dispatcher.include_router(router)


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


@dispatcher.message(Command('help'))
async def send_help(message: Message):
    await bot.send_message(message.chat.id, read_file('help.txt'))


@dispatcher.message(Command('rename'))
async def send_rename(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('rename.txt'))
    await state.set_state(States.change_name_start)


@dispatcher.message(Command('enhance'))
async def send_enhance(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@dispatcher.message(Command('recolor'))
async def send_recolor(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@dispatcher.message(Command('change'))
async def send_change(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@dispatcher.message(Command('generate'))
async def send_generate(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@dispatcher.message(Command('effects'))
async def send_effects(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@dispatcher.message(Command('prices'))
async def send_prices(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


asyncio.run(main())
