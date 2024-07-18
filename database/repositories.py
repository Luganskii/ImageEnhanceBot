import datetime

from sqlalchemy import update as sql_update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import select

from database.dtos import NewSubscriptionDto, SubscriptionDto, UserDto
from database.entities import Subscription, User


class UserRepository:
    def __init__(self, session_maker):
        self._session = session_maker

    def create(self, dto: UserDto) -> int:
        with self._session() as session:
            new_instance: User = User(id=dto.user_id,
                                      username=dto.username,
                                      main_name=dto.main_name,
                                      subscription_id=dto.subscription_id,
                                      language=dto.language,
                                      balance=0,
                                      registration_date=datetime.datetime.now(),
                                      activities=[],
                                      payments_history=[])
            session.add(new_instance)
            session.commit()
            return new_instance.id

    def get_by_id(self, user_id: int) -> User | None:
        with self._session() as session:
            user = session.get(User, user_id)
            return user

    def get_by_username(self, username: str) -> User | None:
        with self._session() as session:
            user = session.scalar(select(User).where(User.username == username))
            return user

    def get_all(self) -> list[User]:
        with self._session() as session:
            users = session.scalars(select(User))
            return list(users)

    def update(self, user_id: int, user_data: User) -> User:
        with self._session() as session:
            user = session.get(User, user_id)

            if not user:
                raise NoResultFound(f'Error: user with id "{user_id}" was not found')

            # SQL-запрос для обновления
            query = sql_update(User).where(User.id == user_id).values(
                username=user_data.username,
                activities=user_data.activities,
                payments_history=user_data.payments_history,
                balance=user_data.balance,
            ).execution_options(synchronize_session='fetch')

            session.execute(query)
            session.commit()
            session.refresh(user)
            return user
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
