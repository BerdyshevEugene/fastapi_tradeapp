from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# создаем приложение
app = FastAPI(
    title='Trade app'
)

# роутер
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

# роутер для регистрации пользователя
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


# создаем точку входа для пользователей, для получения данных
# @app.get('/users/{user_id}', response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in fake_users if user.get('id') == user_id]


# fake_trades = [
#     {'id': 1, 'user_id': 1, 'currency': 'BTC',
#         'side': 'buy', 'price': 123, 'amount': 2.12},
#     {'id': 2, 'user_id': 1, 'currency': 'BTC',
#         'side': 'sell', 'price': 125, 'amount': 2.12},
# ]


# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=5)
#     side: str
#     price: float = Field(ge=0)
#     amount: float


# @app.post('/trades')
# def add_trades(trades: List[Trade]):
#     fake_trades.extend(trades)
#     return {'status': 200, 'data': fake_trades}


# fake_users_2 = [
#     {'id': 1, 'role': 'admin', 'name': 'bob'},
#     {'id': 2, 'role': 'investor', 'name': 'john'},
#     {'id': 3, 'role': 'trader', 'name': 'Matt'},
# ]


# @app.post('/users/{user_id}')
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(
#         filter(lambda user: user.get('id') == user_id, fake_users_2))[0]
#     current_user['name'] = new_name
#     return {'status': 200, 'data': current_user}
