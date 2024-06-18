import logging
from typing import Optional, Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Category, Error, Ok, Exhibit, ExhibitAddDTO, Storage
from annotations.objects import CategoryAddDTO, StorageAddDTO
from common.db.pg_storages import add_storage, get_storage_by_id, get_storage_by_info, update_storage
from common.db.pg_categories import add_category, get_category_by_id, get_category_by_name, update_category
from core.orm import ExhibitsModel
from common.db.pg_exhibits import add_exhibit, get_exhibit_by_id, get_exhibits, update_exhibit, delete_exhibit


class ExhibitsView(PydanticView):

    async def post(self, exhibit: ExhibitAddDTO) -> Union[r200[Exhibit], r500[Error]]:
        """
        Create a new exhibit

        tags: Exhibit

        status codes:
            200: Exhibit created successfully

        """
        
        app = self.request.app

        try:

            result: ExhibitsModel = await add_exhibit(app, exhibit)

            storage = await get_storage_by_id(app, result.storage_id)
            category = await get_category_by_id(app, result.category_id)

            storage = Storage.model_validate(storage)
            category = Category.model_validate(category)

        
        
            return web.json_response(Exhibit(id = result.id, name = result.name, description=result.description, date_of_creation=result.date_of_creation, author=result.author, material=result.material, category=category, storage=storage).to_dict(), status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            ) 
        
    async def get(self, id: Optional[int] = None) -> Union[r200[list[Exhibit]], r500[Error]]:
        """
        Get all exhibits. If id set will return certain exhibit by id. Else return all exhibits in list

        tags: Exhibit
        status codes:
            200: List of exhibits or a certain storage
        """

        app  = self.request.app

        try:
            if id:
                result = await get_exhibit_by_id(app, id)
                logging.debug(result)
                
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)

                storage = await get_storage_by_id(app, result.storage_id)
                category = await get_category_by_id(app, result.category_id)

                storage = Storage.model_validate(storage)
                category = Category.model_validate(category)

                return web.json_response(Exhibit(id = result.id, name = result.name, description=result.description, date_of_creation=result.date_of_creation, author=result.author, material=result.material, category=category, storage=storage).to_dict(), status=200)
            else:
                result: list[ExhibitsModel] = await get_exhibits(app)
                _ = []
                
                for i in result:

                    storage = await get_storage_by_id(app, i.storage_id)
                    category = await get_category_by_id(app, i.category_id)

                    storage = Storage.model_validate(storage)
                    category = Category.model_validate(category)

                    _.append(Exhibit(id = i.id, name = i.name, description=i.description, date_of_creation=i.date_of_creation, author=i.author, material=i.material, category=category, storage=storage).to_dict())

                return web.json_response(_, status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, exhibit: Exhibit) -> Union[r200[Exhibit], r500[Error]]:
        """
        Update a exhibit by id

        tags: Exhibit
        status codes:
            200: Exhibit updated successfully
        """

        app  = self.request.app

        try:

            await update_category(app, exhibit.category)
            await update_storage(app, exhibit.storage)

            result = await update_exhibit(app, exhibit)
            
            storage = await get_storage_by_id(app, result.storage_id)
            category = await get_category_by_id(app, result.category_id)

            storage = Storage.model_validate(storage)
            category = Category.model_validate(category)


            return web.json_response(Exhibit(id = result.id, name = result.name, description=result.description, date_of_creation=result.date_of_creation, author=result.author, material=result.material, category=category, storage=storage).to_dict(), status=200)
       
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a exhibit by number

        tags: Exhibit
        status codes:
            200: Exhibit deleted successfully
        """

        app = self.request.app

        try:
            result: ExhibitsModel = await delete_exhibit(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
