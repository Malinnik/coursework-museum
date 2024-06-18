import logging
from typing import Optional, Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Error, Ok, Activity, ActivityAddDTO
from core.orm import ActivitiesModel
from common.db.pg_activity import add_activity, get_activities, get_activity_by_id, update_activity, delete_activity

class ActivitiesView(PydanticView):

    async def post(self, activity: ActivityAddDTO) -> Union[r200[Activity], r500[Error]]:
        """
        Create a new activity

        tags: Activity

        status codes:
            200: Activity created successfully

        """
        
        app = self.request.app

        # try:
        result: ActivitiesModel = await add_activity(app, activity)
        
        return web.json_response(Activity.model_validate(result).to_dict(), status=200)

        # except Exception as e:
        #     logging.error(e)
        #     return web.json_response(
        #         Error(error="Internal server error").model_dump(), status=500
        #     ) 
        
    async def get(self, id: Optional[int] = None) -> Union[r200[list[Activity]], r500[Error]]:
        """
        Get all Activities. If id set will return certain Activity by id. Else return all Activity in list

        tags: Activity
        status codes:
            200: List of Activities or a certain Activity
        """

        app  = self.request.app

        try:
            if id:
                result: list[Activity]  = await get_activity_by_id(app, id)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(Activity.model_validate(result).to_dict(), status=200)
            else:
                result: list[ActivitiesModel] = await get_activities(app)
                return web.json_response([Activity.model_validate(i).to_dict() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, activity: Activity) -> Union[r200[Activity], r500[Error]]:
        """
        Update a Activity by id

        tags: Activity
        status codes:
            200: Activity updated successfully
        """

        app  = self.request.app

        try:
            result = await update_activity(app, activity)
            return web.json_response(Activity.model_validate(result).to_dict(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a Activity by number

        tags: Activity
        status codes:
            200: Activity deleted successfully
        """

        app = self.request.app

        try:
            result: ActivitiesModel = await delete_activity(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
