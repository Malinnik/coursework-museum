import datetime
from sqlalchemy import ForeignKey, String, Date, Time, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy.dialects.postgresql import UUID

from typing import Annotated

class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
uuidpk = Annotated[UUID, mapped_column(UUID() ,primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now
)]

str_60 = Annotated[str, mapped_column(String(60))]
str_60_unique = Annotated[str, mapped_column(String(60), unique=True)]
str_256 = Annotated[str, mapped_column(String(256))]
str_256_unique  = Annotated[str, mapped_column(String(256), unique=True)]



class RoomsModel(Base):
    __tablename__  =  "rooms"

    room: Mapped[intpk]

class StorageModel(Base):
    __tablename__  =  "storages"

    id: Mapped[intpk]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room"))
    shelf: Mapped[str_256]

class CategoriesModel(Base):
    __tablename__  =  "categories"

    id: Mapped[intpk]
    name: Mapped[str_256]


# class HistoriesModel(Base):
#     __tablename__  =  "histories"

#     id: Mapped[intpk]
#     previous_owner: Mapped[str_256]
#     where_found: Mapped[str_256]

# class RestorationsModel(Base):
#     __tablename__  =  "restorations"

#     id: Mapped[intpk]
#     history_id: Mapped[int]  = mapped_column(ForeignKey("histories.id", ondelete="SET NULL"))
#     staff: Mapped[str_256]
#     date: Mapped[created_at]


class ExhibitsModel(Base):
    __tablename__ = "exhibits"
    
    id: Mapped[intpk]
    name: Mapped[str_60] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    date_of_creation: Mapped[created_at]
    author: Mapped[str_256] = mapped_column(nullable=True) 
    material: Mapped[str_256] = mapped_column(nullable=True)
    storage_id: Mapped[int] = mapped_column(ForeignKey("storages.id", ondelete="SET NULL"))
    # history_id: Mapped[int]  = mapped_column(ForeignKey("histories.id", ondelete="SET NULL"))



class UsersModel(Base):
    __tablename__ = "users"
    
    id: Mapped[intpk]
    username: Mapped[str_60_unique]
    password: Mapped[str] = mapped_column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    fullname: Mapped[str_256]
    email: Mapped[str_60_unique] = mapped_column(nullable=True)
    phone: Mapped[str_60_unique] = mapped_column(nullable=True)
    staff: Mapped[bool] = mapped_column(default=False)


class ActivitiesModel(Base):
    __tablename__  =  "activities"

    id: Mapped[intpk]
    name: Mapped[str_256]
    description: Mapped[str]
    date: Mapped[created_at]

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room"))


class TicketsModel(Base):
    __tablename__  = "tickets"

    id: Mapped[uuidpk] 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    activity_id: Mapped[int]  = mapped_column(ForeignKey("activities.id"))
    cost: Mapped[float]
    date: Mapped[created_at]
    visited: Mapped[bool]


class ReceiptsModel(Base):
    __tablename__  = "receipts"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    acivity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))
    url: Mapped[str]
    date: Mapped[created_at]