import logging

from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from annotations.objects import Room
from core.orm import RoomsModel

async def add_room(app: Application, room: Room) -> RoomsModel:
    """
    Add a new room to the database.
    """

    query = insert(RoomsModel).values(room=room.room).returning(RoomsModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result.first()
    
async def get_all_rooms(app: Application) -> list[RoomsModel]:
    """
    Get all rooms from the database.
    """
    query = select(RoomsModel)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result

async def update_room_number(app: Application, old_number: int, new_number: int)  -> RoomsModel:
    """
    Update room number.
    """
    query = update(RoomsModel).where(RoomsModel.room  == old_number).values(room=new_number).returning(RoomsModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_room(app: Application, room: int) -> RoomsModel:
    """
    Delete a room from the database.
    """
    query = delete(RoomsModel).where(RoomsModel.room == room).returning(RoomsModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()