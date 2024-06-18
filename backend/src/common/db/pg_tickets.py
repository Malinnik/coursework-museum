import logging

from aiohttp.web import Application
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from annotations.objects import TicketAddDTO, Ticket
from core.orm import TicketsModel

async def add_ticket(app: Application, ticket: TicketAddDTO) -> TicketsModel:
    """
    Add a new storage to the database.
    """

    query = insert(TicketsModel).values(user_id=ticket.user, activity_id=ticket.activity, cost=ticket.cost).returning(TicketsModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e

        return result.first()
    
async def get_all_tickets(app: Application) -> list[TicketsModel]:
    """
    Get all storages from the database.
    """
    query = select(TicketsModel)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result

async def get_ticket_by_id(app: Application, id: int) -> TicketsModel:
    """
    Get a storage by its ID from the database.
    """
    query  = select(TicketsModel).where(TicketsModel.id == id)

    async with app['db_engine'].begin() as session:
        result = await session.execute(query)
        return result.first()

async def update_ticket(app: Application, ticket: Ticket) -> TicketsModel:
    """
    Update storage
    """
    query = update(TicketsModel).where(TicketsModel.id  == ticket.id).values(user_id=ticket.user, activity_id=ticket.activity, cost=ticket.cost).returning(TicketsModel)
    
    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()
    

async def delete_ticket(app: Application, id: int) -> TicketsModel:
    """
    Delete a storage from the database.
    """
    query = delete(TicketsModel).where(TicketsModel.id == id).returning(TicketsModel)

    async with app['db_engine'].begin() as session:
        try:
            result = await session.execute(query)
        except IntegrityError as e:
            logging.error(e)
            raise e
        return result.first()

