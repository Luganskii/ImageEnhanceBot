from datetime import datetime

from sqlalchemy import DateTime, Double, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


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
    count_of_params: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    activities: Mapped[list['Activity']] = relationship(back_populates='models')
