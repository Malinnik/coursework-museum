import logging
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from typing import Optional, Union

from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r409, r500

from annotations.objects import Ok, Error, UserAddDTO, User, UsersTable
from common.db.pg_users import add_user, get_user_by_id, get_user_by_username, get_users, update_user, delete_user
from core.orm import UsersModel


class UserView(PydanticView):

    async def post(self, user: UserAddDTO) -> Union[r201[Ok], r409[Error]]:
        """
        Add a new user

        tags: User
        status codes:
            201: User added successfully
            400: Bad request
            409: User already exists
        """ 
        app = self.request.app

        if len(user.password.get_secret_value()) < 8:
            return web.json_response(
                Error(error="Password must be at least 8 characters long").model_dump(),
                status=400
            )

        try:
            result = await add_user(app, user)
        except IntegrityError:
            return web.json_response(Error(error="User already exists").model_dump(), status=409)


        if result:
            return web.json_response(Ok(ok="User added successfully").model_dump(), status=201)
        
        return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
        )
    
    async def get(self, id: Optional[int] = None, username: Optional[str] = None) -> Union[r201[Ok], r409[Error]]:
        """
        Get a user

        tags: User
        
        status codes:
            200: User 
            400: Bad request
        """

        app  = self.request.app

        try:
            if id:
                result: User  = await get_user_by_id(app, id)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(UsersTable.model_validate(result).model_dump(), status=200)
            
            if username:
                result: User  = await get_user_by_username(app, username)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(UsersTable.model_validate(result).model_dump(), status=200)

            else:
                result: list[UsersModel] = await get_users(app)
                return web.json_response([UsersTable.model_validate(i).model_dump() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
        )


    async def put(self, user: User) -> Union[r201[Ok], r500[Error]]:
        """
        Update a user

        tags: User
        status codes:
            200: User updated successfully
        """

        app  = self.request.app

        try:
            if len(user.password.get_secret_value()) < 8:
                return web.json_response(
                    Error(error="Password must be at least 8 characters long").model_dump(),
                    status=400
                )
            
            result = await update_user(app, user)


            return web.json_response(Ok().model_dump(), status=201)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a User by id

        tags: User
        status codes:
            200: User deleted successfully
        """

        app = self.request.app

        try:
            result: UsersModel = await delete_storage(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
