from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDto:
    user_id: int
    username: str
    main_name: str
    language: str
    subscription_id: int
    balance: float
    registration_date: datetime
    activities: list
    payments_history: list


@dataclass
class SubscriptionDto:
    subscription_id: int
    description: str
    price: float


@dataclass
class NewSubscriptionDto:
    description: str
    price: float
