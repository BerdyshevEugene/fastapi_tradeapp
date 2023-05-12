from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.response import JSONResponse

# создаем приложение
app = FastAPI(
    title='Trading app'
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'bob'},
    {'id': 2, 'role': 'investor', 'name': 'john'},
    {'id': 3, 'role': 'trader', 'name': 'Matt'},
    {'id': 4, 'role': 'investor', 'name': 'Homer', 'degree': [
        {'id': 1, 'created_at': '2019-06-24T09:00', 'type_degree': 'expert'}
    ]},
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


# создаем точку входа для пользователей, для получения данных
@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC',
        'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC',
        'side': 'sell', 'price': 125, 'amount': 2.12},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}


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
