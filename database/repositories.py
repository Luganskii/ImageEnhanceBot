from sqlalchemy import update as sql_update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select

from database.dtos import NewSubscriptionDto, SubscriptionDto, UserDto
from database.entities import Subscription, User


class UserRepository:
    def __init__(self, session_maker):
        self._session = session_maker

    def create(self, dto: UserDto) -> UserDto:
        with self._session() as session:
            new_instance: User = User(id=dto.user_id,
                                      username=dto.username,
                                      main_name=dto.main_name,
                                      subscription_id=dto.subscription_id,
                                      language=dto.language,
                                      balance=dto.balance,
                                      registration_date=dto.registration_date,
                                      activities=dto.activities,
                                      payments_history=dto.payments_history)
            session.add(new_instance)
            session.commit()
            return new_instance.map_to_dto()

    def get_by_id(self, user_id: int) -> UserDto | None:
        with self._session() as session:
            user = session.get(User, user_id)
            return user.map_to_dto() if user is not None else None

    def get_by_username(self, username: str) -> User | None:
        with self._session() as session:
            user = session.scalar(select(User).where(User.username == username))
            return user.map_to_dto()

    def get_all(self) -> list[User]:
        with self._session() as session:
            users = session.scalars(select(User))
            return [user.map_to_dto() if user is not None else None for user in users]

    def update(self, user_id: int, user_data: UserDto) -> User:
        with self._session() as session:
            user = session.get(User, user_id)

            if not user:
                raise NoResultFound(f'Error: user with id "{user_id}" was not found')

            # SQL-запрос для обновления
            query = sql_update(User).where(User.id == user_id).values(
                main_name=user_data.main_name,
                username=user_data.username,
                balance=user_data.balance,
                subscription_id=user_data.subscription_id
            ).execution_options(synchronize_session='fetch')

            session.execute(query)
            session.commit()
            session.refresh(user)
            return user.map_to_dto()
    #
    # async def delete(self, user_id: int) -> bool:
    #     async with self._session() as session:
    #         await session.execute(sql_delete(User).where(User.id == user_id))
    #         await session.commit()
    #         return True


class SubscriptionRepository:
    def __init__(self, session_maker: sessionmaker[Session]):
        self._session = session_maker

    def create(self, sub: NewSubscriptionDto) -> SubscriptionDto:
        with self._session() as session:
            new_instance = Subscription(description=sub.description, price=sub.price)
            session.add(new_instance)
            session.commit()
            return SubscriptionDto(new_instance.id, new_instance.description, new_instance.price)
