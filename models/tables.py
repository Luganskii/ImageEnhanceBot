from datetime import date

from base import Base
from sqlalchemy import Date, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subscription: Mapped[int] = mapped_column(Integer, ForeignKey('subscription.id'), nullable=False)
    language: Mapped[str] = mapped_column(String(3), nullable=False, default='eng')
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())

    subscription_history: Mapped[list['SubscriptionHistory']] = relationship(back_populates='user')
    activity: Mapped[list['Activity']] = relationship(back_populates='user')


class SubscriptionHistory(Base):
    __tablename__ = 'subscription_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    type_subscription: Mapped[int] = mapped_column(Integer, ForeignKey('subscription.id'), nullable=False)
    paid: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped['User'] = relationship(back_populates='subscription_history')
    subscription: Mapped['Subscription'] = relationship(back_populates='subscription_history')


class Subscription(Base):
    __tablename__ = 'subscription'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    subscription_history: Mapped[list['SubscriptionHistory']] = relationship(back_populates='subscription')


class Activity(Base):
    __tablename__ = 'activity'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    model: Mapped[str] = mapped_column(String(10), ForeignKey('models.id'), nullable=False)

    models: Mapped['Models'] = relationship(back_populates='activity')
    user: Mapped['User'] = relationship(back_populates='activity')


class Models(Base):
    __tablename__ = 'models'

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    count_of_params: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)

    activity: Mapped[list['Activity']] = relationship(back_populates='models')
