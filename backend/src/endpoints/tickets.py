import logging
from typing import Optional, Union

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r500

from annotations.objects import Error, Ok, Ticket, TicketAddDTO
from core.orm import TicketsModel
from common.db.pg_tickets import add_ticket, get_all_tickets, get_ticket_by_id, update_ticket, delete_ticket


class TicketsView(PydanticView):

    async def post(self, ticket: TicketAddDTO) -> Union[r200[Ticket], r500[Error]]:
        """
        Create a new Ticket

        tags: Ticket

        status codes:
            200: Ticket created successfully

        """
        
        app = self.request.app

        try:
            result: TicketsModel = await add_ticket(app, ticket)
            
            return web.json_response(Ticket.model_validate(result).to_dict(), status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            ) 
        
    async def get(self, id: Optional[int] = None) -> Union[r200[list[Ticket]], r500[Error]]:
        """
        Get all Tickets. If id set will return certain Ticket by id. Else return all Tickets in list

        tags: Ticket
        status codes:
            200: List of Tickets or a certain Ticket
        """

        app  = self.request.app

        try:
            if id:
                result: TicketsModel = await get_ticket_by_id(app, id)
                if not result:
                    return web.json_response(Error(error="Not Found").model_dump(), status=404)
                return web.json_response(Ticket.model_validate(result).to_dict(), status=200)
            else:
                result: list[TicketsModel] = await get_all_tickets(app)
                return web.json_response([Ticket.model_validate(i).to_dict() for i in result], status=200)

        except Exception as e:
            logging.error(e)
            return web.json_response(
                Error(error="Internal server error").model_dump(), status=500
            )


    async def put(self, ticket: Ticket) -> Union[r200[Ticket], r500[Error]]:
        """
        Update a Ticket by id

        tags: Ticket
        status codes:
            200: Ticket updated successfully
        """

        app  = self.request.app

        try:
            result = await update_ticket(app, ticket)
            return web.json_response(Ticket.model_validate(result).to_dict(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(
            Error(error="Internal server error").model_dump(), status=500
            )


    async def delete(self, id: int) -> Union[r200[Ok], r500[Error]]:
        """
        Delete a Ticket by number

        tags: Ticket
        status codes:
            200: Ticket deleted successfully
        """

        app = self.request.app

        try:
            result: TicketsModel = await delete_ticket(app, id)
            return web.json_response(Ok().model_dump(), status=200)
        except Exception as e:
            logging.error(e)
            return web.json_response(Error(error="Internal server error").model_dump(), status=500)
