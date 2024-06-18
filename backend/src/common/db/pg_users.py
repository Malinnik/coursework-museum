import logging
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from aiohttp.web import Application

from annotations.objects import UserAddDTO, User
from core.orm import UsersModel


async def add_user(app: Application, user: UserAddDTO) -> int:
    query = insert(UsersModel).values(username=user.username, password=user.password.get_secret_value(), fullname=user.fullname, staff=user.staff).returning(UsersModel.id)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result

async def get_users(app: Application) -> list[UsersModel]:
    query = select(UsersModel)
    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result


async def get_user_by_username(app: Application, username: str) -> UsersModel:
    query = select(UsersModel).where(UsersModel.username == username)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def get_user_by_id(app: Application, user_id: int) -> UsersModel:
    query = select(UsersModel).where(UsersModel.id == user_id)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()
    

async def update_user(app: Application, user: User) -> UsersModel:
    """
    Update storage
    """
    query = update(UsersModel).where(UsersModel.id  == user.id).values(username=user.username, password=user.password.get_secret_value(), fullname=user.fullname, email=user.email, phone=user.phone, staff=user.staff).returning(UsersModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_user(app: Application, id: int) -> UsersModel:
    """
    Delete a storage from the database.
    """
    query = delete(UsersModel).where(UsersModel.id == id).returning(UsersModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()

