from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.phrases_interpreter import read_file, read_placeholder_file
from bot.states import States
from database.config import session_maker
from database.repositories import UserRepository

command_router = Router()

user_repository = UserRepository(session_maker=session_maker)


@command_router.message(Command('start'))
async def send_welcome(message: Message, state: FSMContext) -> None:
    if not user_repository.get_by_id(message.from_user.id):
        await message.answer(read_file('first_greeting.txt'))
        await state.set_state(States.registration_start)
    else:
        await message.answer(await read_placeholder_file('again_greeting.txt', message.from_user.id))


@command_router.message(Command('help'))
async def send_help(message: Message):
    await message.answer(read_file('help.txt'))


@command_router.message(Command('rename'))
async def send_rename(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('rename.txt'))
    await state.set_state(States.change_name_start)


@command_router.message(Command('enhance'))
async def send_enhance(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))
    await state.set_state(States.enhance_start)


@command_router.message(Command('recolor'))
async def send_recolor(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@command_router.message(Command('change'))
async def send_change(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@command_router.message(Command('generate'))
async def send_generate(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@command_router.message(Command('effects'))
async def send_effects(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))


@command_router.message(Command('prices'))
async def send_prices(message: Message, state: FSMContext) -> None:
    await message.answer(read_file('not_implemented.txt'))
