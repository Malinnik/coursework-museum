import logging

from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from annotations.objects import Activity, ActivityAddDTO
from core.orm import ActivitiesModel

async def add_activity(app: Application, activity: ActivityAddDTO) -> ActivitiesModel:
    """
    Add a new activity to the database.
    """

    query = insert(ActivitiesModel).values(name=activity.name, description=activity.description, date=activity.date, room_id=activity.room).returning(ActivitiesModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result.first()
    
async def get_activities(app: Application) -> list[ActivitiesModel]:
    """
    Get all activities from the database.
    """
    query = select(ActivitiesModel)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result

async def get_activity_by_id(app: Application, id: int) -> ActivitiesModel:
    """
    Get a activity by its ID from the database.
    """
    query  = select(ActivitiesModel).where(ActivitiesModel.id == id)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def update_activity(app: Application, activity: Activity) -> ActivitiesModel:
    """
    Update activity to the database.
    """
    query = update(ActivitiesModel).where(ActivitiesModel.id  == activity.id).values(name=activity.name, description=activity.description, date=activity.date, room_id=activity.room).returning(ActivitiesModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_activity(app: Application, id: int) -> ActivitiesModel:
    """
    Delete a activity from the database.
    """
    query = delete(ActivitiesModel).where(ActivitiesModel.id == id).returning(ActivitiesModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()

