from datetime import datetime

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from bot.config import (
    srgan_x2_image_processor,
    srgan_x4_image_processor,
    srgan_x8_image_processor,
)
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


@simple_states_router.message(StateFilter(States.enhance_start_x2))
async def enhance_image_x2(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')
    date = f"{datetime.now().strftime('%d-%H-%M-%S')}"
    await message.bot.download(file=message.document.file_id, destination=f"/app/media/lr_{date}_{message.document.file_id}.jpg")
    await message.answer_document(caption=read_file('enhance_success.txt'),
                                  document=FSInputFile(srgan_x2_image_processor.update(path_to_picture=f"/app/media/lr_{date}_{message.document.file_id}.jpg")))
    await state.clear()


@simple_states_router.message(StateFilter(States.enhance_start_x4))
async def enhance_image_x4(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')
    date = f"{datetime.now().strftime('%d-%H-%M-%S')}"
    await message.bot.download(file=message.document.file_id, destination=f"/app/media/lr_{date}_{message.document.file_id}.jpg")
    await message.answer_document(caption=read_file('enhance_success.txt'),
                                  document=FSInputFile(srgan_x4_image_processor.update(path_to_picture=f"/app/media/lr_{date}_{message.document.file_id}.jpg")))
    await state.clear()


@simple_states_router.message(StateFilter(States.enhance_start_x8))
async def enhance_image_x8(message: Message, state: FSMContext) -> None:
    user = user_repository.get_by_id(message.from_user.id)
    if user is None:
        raise Exception('user not found')
    date = f"{datetime.now().strftime('%d-%H-%M-%S')}"
    await message.bot.download(file=message.document.file_id, destination=f"/app/media/lr_{date}_{message.document.file_id}.jpg")
    await message.answer_document(caption=read_file('enhance_success.txt'),
                                  document=FSInputFile(srgan_x8_image_processor.update(path_to_picture=f"/app/media/lr_{date}_{message.document.file_id}.jpg")))
    await state.clear()
