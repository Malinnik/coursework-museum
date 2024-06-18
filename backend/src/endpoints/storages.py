import logging
from typing import Optional, Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Error, Ok, Storage, StorageAddDTO
from core.orm import CategoriesModel
from common.db.pg_storages import add_storage, get_all_storages, get_storage_by_id, update_storage, delete_storage


class StorageView(PydanticView):

    async def post(self, storage: StorageAddDTO) -> Union[r200[Storage], r500[Error]]:
        """
        Create a new storage

        tags: Storage

        status codes:
            200: Storage created successfully

        """
        
        app = self.request.app

        try:
            result: CategoriesModel = await add_storage(app, storage)
            
            return web.json_response(Storage.model_validate(result).model_dump(), status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            ) 
        
    async def get(self, id: Optional[int] = None) -> Union[r200[list[Storage]], r500[Error]]:
        """
        Get all Storagies. If id set will return certain storage by id. Else return all storagies in list

        tags: Storage
        status codes:
            200: List of storagies or a certain storage
        """

        app  = self.request.app

        try:
            if id:
                result: list[Storage]  = await get_storage_by_id(app, id)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(Storage.model_validate(result).model_dump(), status=200)
            else:
                result: list[CategoriesModel] = await get_all_storages(app)
                return web.json_response([Storage.model_validate(i).model_dump() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, storage: Storage) -> Union[r200[Storage], r500[Error]]:
        """
        Update a storage by id

        tags: Storage
        status codes:
            200: Storage updated successfully
        """

        app  = self.request.app

        try:
            result = await update_storage(app, storage)
            return web.json_response(Storage.model_validate(result).model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a storage by number

        tags: Storage
        status codes:
            200: Storage deleted successfully
        """

        app = self.request.app

        try:
            result: CategoriesModel = await delete_storage(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
