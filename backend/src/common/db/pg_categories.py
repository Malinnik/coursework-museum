import logging

from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from annotations.objects import Category, CategoryAddDTO
from core.orm import CategoriesModel

async def add_category(app: Application, category: CategoryAddDTO) -> CategoriesModel:
    """
    Add a new category to the database.
    """

    query = insert(CategoriesModel).values(name=category.name).returning(CategoriesModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result.first()
    
async def get_all_categories(app: Application) -> list[CategoriesModel]:
    """
    Get all categories from the database.
    """
    query = select(CategoriesModel)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result

async def get_category_by_id(app: Application, id: int) -> CategoriesModel:
    """
    Get a category by its ID from the database.
    """
    query  = select(CategoriesModel).where(CategoriesModel.id == id)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()
    
async def get_category_by_name(app: Application, name: str) -> CategoriesModel:
    """
    Get a category by its ID from the database.
    """
    query  = select(CategoriesModel).where(CategoriesModel.name == name)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def update_category(app: Application, category: Category) -> CategoriesModel:
    """
    Set the name of a category.
    """
    query = update(CategoriesModel).where(CategoriesModel.id  == category.id).values(name=category.name).returning(CategoriesModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_category(app: Application, id: int) -> CategoriesModel:
    """
    Delete a category from the database.
    """
    query = delete(CategoriesModel).where(CategoriesModel.id == id).returning(CategoriesModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()

