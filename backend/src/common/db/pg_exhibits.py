import logging
from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update

from annotations.objects import Exhibit, ExhibitAddDTO
from core.orm import ExhibitsModel



async def add_exhibit(app: Application, exhibit: ExhibitAddDTO) -> ExhibitsModel:
    """
    Add an exhibit to the application.
    """

    query = insert(ExhibitsModel).values(
        exhibit.to_dict(),
    ).returning(ExhibitsModel)

    # query = insert(ExhibitsModel).values(
    #     name=exhibit.name,
    #     description=exhibit.description,
    #     category_id=exhibit.category_id,
    #     date_of_creation=exhibit.date_of_creation,
    #     author=exhibit.author,
    #     material=exhibit.material,
    #     storage_id=exhibit.storage_id,
    # ).returning(ExhibitsModel)

    async with app["db_engine"].begin() as session:
        try:
            result = await session.execute(query)
        except Exception as e:
            logging.error(e)
            raise e
        
        return result.first()


async def update_exhibit(app: Application, exhibit: Exhibit) -> ExhibitsModel:
    """
    Edit an exhibit in the application.
    """

    query = update(ExhibitsModel).where(ExhibitsModel.id == exhibit.id).values(
        name=exhibit.name,
        description=exhibit.description,
        # category_id=exhibit.category.id,
        date_of_creation=exhibit.date_of_creation,
        author=exhibit.author,
        material=exhibit.material,
        # storage_id=exhibit.storage.id
    ).returning(ExhibitsModel)

    async with app["db_engine"].begin() as session:
        try:
            result  = await session.execute(query)
        except Exception as e:
            logging.error(e)
            raise e
        return result.first()


async def get_exhibits(app: Application) -> list[ExhibitsModel]:
    """

    """
    query = select(ExhibitsModel)
    
    async with app["db_engine"].begin() as session:
        try:
            result = await session.execute(query)
        except Exception as e:
            logging.error(e)
            raise e
        return result


async def get_exhibit_by_id(app: Application, id: int)  -> ExhibitsModel:
    """
    Get an exhibit by its id.
    """

    query  = select(ExhibitsModel).where(ExhibitsModel.id  == id)

    async with app["db_engine"].begin() as session:
        try:
            result = await session.execute(query)
        except Exception as e:
            logging.error(e)
            raise e
        return result.first()

async def delete_exhibit(app: Application, id: int) -> ExhibitsModel:
    """
    Delete an exhibit by its id.
    """

    query = delete(ExhibitsModel).where(ExhibitsModel.id == id).returning(ExhibitsModel)

    async with app["db_engine"].begin() as session:
        try:
            result  = await session.execute(query)
        except Exception as e:
            logging.error(e)
            raise e
        return result.first()


