from aiohttp import web

from endpoints.tickets import TicketsView
from endpoints.activities import ActivitiesView
from endpoints.exhibits import ExhibitsView
from endpoints.storages import StorageView
from endpoints.categories import CategoryView
from endpoints.rooms import RoomView
from endpoints.authentification import Check, Login
from endpoints.users import UserView

def setup_routes(app: web.Application):
    """Инициализация роутов"""
    app.add_routes(
        [
            # User
            web.view('/api/v1/users', UserView),
            
            # Room
            web.view('/api/v1/rooms', RoomView),

            # Category
            web.view('/api/v1/categories', CategoryView),

            # Storage
            web.view('/api/v1/storage', StorageView),

            # Exhibits
            web.view('/api/v1/exhibits', ExhibitsView),

            # Activity
            web.view('/api/v1/activity', ActivitiesView),

            # Ticket
            web.view('/api/v1/tickets', TicketsView),

            # Auth
            web.view('/api/v1/login', Login),
            web.view('/api/v1/check', Check),
        ]
)