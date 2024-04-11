from fastapi import FastAPI
from typing import Union
from schemas import CreateUser, ReadUser
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from models import User
from sqlalchemy import select
from typing import List
app = FastAPI()

@app.get("/")
async def hello():
    return{"Hello": "World"}

@app.post('/user')
async def add_user(user:CreateUser):
    async with AsyncSession(engine) as session:
        new_user = User(name = user.name, fullname = user.fullname, nickname = user.nickname)
        session.add(new_user)
        await session.commit()
        return{"Status": "Success"}

#:param offset: сколько пропускаем
#:param limit: сколько берём



@app.get('/user') # получить всех юзеров
async def user_list(offset:int, limit:int) -> List[ReadUser]:
    async with AsyncSession(engine) as session:
        stmt = select(User).limit(limit).offset(offset)
        result = await session.scalars(stmt)
        users = result.all() # приводит ответ алхимии к объектам питона
    return users

@app.get('/user/{user_id}')
async def get_user(user_id:int) -> ReadUser:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.scalars(stmt)
    return result.first()

@app.delete('/user/{user_id}')
async def delete_user(user_id:int) -> dict:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.scalars(stmt)
        user =  result.first()
        await session.delete(user)
        await session.commit()
    return {'status': 'OK'}

users = {}
@app.put('/user')
#async def update_user()pass #обновить все данные пользователя
async def update_user(user_id: int, updated_data: dict):
    if user_id in users:
        users[user_id].update(updated_data)


#@app.patch()
#async def update_user():pass #смена никнейма
