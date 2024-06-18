import logging
from aiohttp import web

from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r400, r401, r500
from typing import Union

from annotations.objects import Error, Ok, User, UserAddDTO
from common.db.pg_users import get_user_by_username
from common.logger.jwt_config import decode_access, encode_access


class Login(PydanticView):

    async def post(self, user: UserAddDTO) -> Union[r200[str], r400[Error]]:
        """
        User login

        tags: Auth
        status codes:
            200: User authentificated successfully
            400: Bad request
        """
        app = self.request.app

        try:
            check = await get_user_by_username(app, user.username)

            if not check:
                return web.json_response(Error(error="Неправильный логин или пароль").model_dump(), status=400)

            if (not user.password.get_secret_value() == check.password):
                return web.json_response(Error(error="Неправильный логин или пароль").model_dump(), status=400)
            

            access = await encode_access(app, check.id)

            response = web.json_response({"user_token": access, "user_id": check.id}, status=200)

            # TODO: Make refresh token encoding and sending it to cookie
            # refresh
            # response.set_cookie()

            logging.info(f"User auth: {user.username}")
            return response

        except Exception as e:
            logging.exception(f"Error: {e}")
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )

class Check(PydanticView):
    async def get(self) -> Union[r200[Ok], r401[Error], r500[Error]]:
        """
        Check user authorization
        tags: Auth
        status codes:
            200: User authentificated successfully
            401: User unauthorized
            500: Internal server error
        """
        app = self.request.app
        try:
            access = self.request.headers.get("Authorization")
            logging.debug(f"Access:  {access}")
            if not access:
                return web.json_response(Error(error="No access token").model_dump(), status=401)
            
            await decode_access(app, access)
            logging.debug(f"Access:  {access}")

            return web.json_response(Ok().model_dump(), status=201)            

        except web.HTTPUnauthorized:
            logging.debug(f"Access:  Access token expired")
            raise web.HTTPFound('/login')
            return web.json_response(Error(error="Access token expired").model_dump(), status=401)
        except Exception as e:
            logging.exception(f"Error: {e}")
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )

class Refresh(PydanticView):
    pass