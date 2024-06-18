import logging
from typing import Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Error, Ok, Room, UpdateRoomDTO
from core.orm import RoomsModel
from common.db.pg_room import add_room, delete_room, get_all_rooms, update_room_number

class RoomView(PydanticView):

    async def post(self, room: Room) -> Union[r200[Room], r500[Error]]:
        """
        Create a new room

        tags: Room

        status codes:
            200: Room created successfully

        """
        
        app = self.request.app

        try:
            result: RoomsModel = await add_room(app, room)
            
            return web.json_response(Room.model_validate(result).model_dump(), status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            ) 
        
    async def get(self) -> Union[r200[list[Room]], r500[Error]]:
        """
        Get all rooms

        tags: Room
        status codes:
            200: List of rooms
        """

        app  = self.request.app

        try:
            result: list[RoomsModel] = await get_all_rooms(app)
            logging.debug(f"get_rooms: {result=}")
            return web.json_response([Room.model_validate(i).model_dump() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, update: UpdateRoomDTO) -> Union[r200[Room], r500[Error]]:
        """
        Update a room by number

        tags: Room
        status codes:
            200: Room number updated successfully
        """

        app  = self.request.app

        try:
            result = await update_room_number(app, update.old_room, update.new_room)
            return web.json_response(Room.model_validate(result).model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, number: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a room by number

        tags: Room
        status codes:
            200: Room deleted successfully
        """

        app = self.request.app

        try:
            result: RoomsModel = await delete_room(app, number)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
