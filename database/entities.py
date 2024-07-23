from datetime import datetime

from sqlalchemy import Boolean, DateTime, Double, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .dtos import UserDto


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey('subscriptions.id'), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    main_name: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False, default='eng')
    balance: Mapped[float] = mapped_column(Double, nullable=False, default=0.0)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    subscriptions: Mapped[list['Subscription']] = relationship(back_populates='users')
    payments_history: Mapped[list['PaymentHistory']] = relationship(back_populates='users')
    activities: Mapped[list['Activity']] = relationship(back_populates='users')
    files: Mapped[list['File']] = relationship(back_populates='users')

    def map_to_dto(self):
        return UserDto(user_id=self.id, subscription_id=self.subscription_id, username=self.username,
                       main_name=self.main_name, language=self.language, balance=self.balance,
                       registration_date=self.registration_date,
                       payments_history=self.payments_history, activities=self.activities)


class PaymentHistory(Base):
    __tablename__ = 'payments_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, ForeignKey('subscriptions.id'), nullable=False)
    paid: Mapped[float] = mapped_column(Double, nullable=False)

    users: Mapped['User'] = relationship(back_populates='payments_history')
    subscriptions: Mapped['Subscription'] = relationship(back_populates='payments_history')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Double, nullable=False, default=0.0)

    users: Mapped[list['User']] = relationship(back_populates='subscriptions')
    payments_history: Mapped[list['PaymentHistory']] = relationship(back_populates='subscriptions')


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_date())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'), nullable=False)

    models: Mapped['Model'] = relationship(back_populates='activities')
    users: Mapped['User'] = relationship(back_populates='activities')


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    params_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    activities: Mapped[list['Activity']] = relationship(back_populates='models')


class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    sent_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # TODO: implement parameters
    is_processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    processing_model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'), nullable=True)
    processed_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    owner: Mapped['User'] = relationship(back_populates='files')
