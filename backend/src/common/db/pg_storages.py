import logging

from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from annotations.objects import StorageAddDTO, Storage
from core.orm import StorageModel

async def add_storage(app: Application, storage: StorageAddDTO) -> StorageModel:
    """
    Add a new storage to the database.
    """

    query = insert(StorageModel).values(room_id=storage.room_id, shelf=storage.shelf).returning(StorageModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result.first()
    
async def get_all_storages(app: Application) -> list[StorageModel]:
    """
    Get all storages from the database.
    """
    query = select(StorageModel)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result

async def get_storage_by_id(app: Application, id: int) -> StorageModel:
    """
    Get a storage by its ID from the database.
    """
    query  = select(StorageModel).where(StorageModel.id == id)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def get_storage_by_info(app: Application, room: int, shelf: str)  -> StorageModel:
    """
    Get a storage by its room and shelf from the database.
    """
    query  = select(StorageModel).where(StorageModel.room_id == room and StorageModel.shelf == shelf)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def update_storage(app: Application, storage: Storage) -> StorageModel:
    """
    Update storage
    """
    query = update(StorageModel).where(StorageModel.id  == storage.id).values(room_id=storage.room_id, shelf=storage.shelf).returning(StorageModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_storage(app: Application, id: int) -> StorageModel:
    """
    Delete a storage from the database.
    """
    query = delete(StorageModel).where(StorageModel.id == id).returning(StorageModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()

