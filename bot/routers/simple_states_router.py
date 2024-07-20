from datetime import datetime

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from bot.phrases_interpreter import read_file, read_placeholder_file
from bot.states import States
from database.config import session_maker
from database.dtos import NewSubscriptionDto, SubscriptionDto, UserDto
from database.repositories import SubscriptionRepository, UserRepository

simple_states_router = Router()


user_repository = UserRepository(session_maker=session_maker)
subscription_repository = SubscriptionRepository(session_maker=session_maker)


@simple_states_router.message(StateFilter(States.registration_start))
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

    await message.answer(await read_placeholder_file('after_name.txt', message.from_user.id) + '\n' + read_file('help.txt'))
    await state.clear()


@simple_states_router.message(StateFilter(States.change_name_start))
async def change_name(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')
    user.main_name = message.text
    user_repository.update(message.from_user.id, user)

    await message.answer(await read_placeholder_file('rename_success.txt', message.from_user.id))
    await state.clear()


@simple_states_router.message(StateFilter(States.enhance_start))
async def enhance_image(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')

    await message.answer_photo(caption=read_file('enhance_success.txt'),
                               photo=FSInputFile('/app/bot/images/default.jpg'))
    await state.clear()
