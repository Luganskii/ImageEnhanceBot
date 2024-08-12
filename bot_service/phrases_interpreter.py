from datetime import datetime

import database.config
from database.repositories import UserRepository

user_repository = UserRepository(database.config.session_maker)


def read_file(file_name: str) -> str:
    with open('/app/bot_service/phrases/' + file_name) as f:
        return f.read()


async def read_placeholder_file(file_name: str, user_id: int) -> str:
    text = read_file(file_name)
    replacements = await get_replace_dict(user_id)
    for word, replacement in replacements.items():
        text = text.replace(word, replacement)
    return text


async def get_replace_dict(user_id: int) -> dict:
    result = dict()
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception('User was not found')
    result['<USER>'] = user.main_name
    result['<CURRENT_DATE>'] = datetime.now().strftime('%d/%m/%Y')
    return result
