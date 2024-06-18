import logging
from typing import Optional, Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Error, Ok, Category, CategoryAddDTO
from core.orm import CategoriesModel
from common.db.pg_categories import add_category, update_category, get_all_categories, get_category_by_id, delete_category

class CategoryView(PydanticView):

    async def post(self, category: CategoryAddDTO) -> Union[r200[Category], r500[Error]]:
        """
        Create a new category

        tags: Category

        status codes:
            200: Category created successfully

        """
        
        app = self.request.app

        try:
            result: CategoriesModel = await add_category(app, category)
            
            return web.json_response(Category.model_validate(result).model_dump(), status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            ) 
        
    async def get(self, id: Optional[int] = None) -> Union[r200[list[Category]], r500[Error]]:
        """
        Get all Categories. If id set will return certain category by id. Else return all categories in list

        tags: Category
        status codes:
            200: List of categories
        """

        app  = self.request.app

        try:
            if id:
                result: list[Category]  = await get_category_by_id(app, id)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(Category.model_validate(result).model_dump(), status=200)
            else:
                result: list[CategoriesModel] = await get_all_categories(app)
                return web.json_response([Category.model_validate(i).model_dump() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, category: Category) -> Union[r200[Category], r500[Error]]:
        """
        Update a category by id

        tags: Category
        status codes:
            200: Category updated successfully
        """

        app  = self.request.app

        try:
            result = await update_category(app, category)
            return web.json_response(Category.model_validate(result).model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a category by number

        tags: Category
        status codes:
            200: Category deleted successfully
        """

        app = self.request.app

        try:
            result: CategoriesModel = await delete_category(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
