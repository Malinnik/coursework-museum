from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4, HttpUrl, Secret


class UserAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    fullname: str
    password: Secret[str]
    staff: bool = False

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    password: Secret[str]
    fullname: str
    email: EmailStr | None = None
    phone: str  | None  = None
    staff: bool = False

class UsersTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    fullname: str
    email: EmailStr | None = None
    phone: str  | None  = None
    staff: bool = False


class HistoryAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    previous_owner: str = Field(max_length=256)
    where_found: str = Field(max_length=256)

class History(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    previous_owner: str = Field(max_length=256)
    where_found: str = Field(max_length=256)


class ResorationAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    history_id: int
    staff: str = Field(max_length=256)
    date: Optional[datetime] = datetime.now()

    def to_dict(self):
        return {
            "history_id": self.history_id,
            "staff": self.staff,
            "date": str(self.date),
    }

class Restoraion(BaseModel):
    id: int
    history_id: int
    staff: str = Field(max_length=256)
    date: Optional[datetime] = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "history_id": self.history_id,
            "staff": self.staff,
            "date": str(self.date),
    }


class StorageAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    room_id: int
    shelf: str = Field(description="Shelf name", max_length=256)

class Storage(BaseModel):
    model_config  = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    shelf: str = Field(description="Shelf name", max_length=256)


class Room(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room: int = Field(gt=0)

class UpdateRoomDTO(BaseModel):
    old_room: int = Field(gt=0)
    new_room: int = Field(gt=0)


class CategoryAddDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(description="Category name", max_length=256)

class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str = Field(description="Category name", max_length=256)




class ExhibitAddDTO(BaseModel):

    name: str = Field(description="Exhibit name", max_length=60)
    description: str
    date_of_creation: Optional[datetime] = datetime.now()
    author: Optional[str] = Field(description="Author name", max_length=256, default=None)
    material: Optional[str] = Field(max_length=256,default=None)
    category_id:  int
    storage_id: int


    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "date_of_creation": self.date_of_creation,
            "author": self.author,
            "material": self.material,
            "category_id": self.category_id,
            "storage_id": self.storage_id,
        }

class Exhibit(BaseModel):
    model_config  = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(description="Exhibit name", max_length=60)
    description: Optional[str]
    date_of_creation: Optional[datetime] = datetime.now()
    author: Optional[str] = Field(description="Author name", max_length=256)
    material: Optional[str] = Field(max_length=256)
    
    category: Category
    storage: Storage


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_of_creation": str(self.date_of_creation),
            "author": self.author,
            "material": self.material,
            
            "category": self.category.model_dump(),
            "storage": self.storage.model_dump(),
        }



class ActivityAddDTO(BaseModel):
    
    name: str = Field(description="Activity name", max_length=256)
    description: str
    date: Optional[datetime] = datetime.now()
    room: int = Field(gt=0)

class Activity(BaseModel):
    model_config  = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(description="Activity name", max_length=256)
    description: str
    date: Optional[datetime] = datetime.now()
    room_id: int = Field(gt=0)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": str(self.date),
            "room_id": self.room_id,
        }




class TicketAddDTO(BaseModel):
    user: int | User
    activity: int  | Activity
    cost: float

class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID4
    user: int | User
    activity: int  | Activity
    cost: float
    date: datetime
    visited: bool

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "user": self.user,
            "activity": self.activity,
            "cost": self.cost,
            "ticket": self.ticket,
            "date": str(self.date),
            "visited": self.visited,
        }




class ReceiptAddDTO(BaseModel):
    user: int | User
    ticket: int | Ticket
    activity: int | Activity

class Receipt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: int | User
    ticket: int | Ticket
    activity: int | Activity
    url: HttpUrl
    date: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "ticket": self.ticket,
            "activity": self.activity,
            "url": self.url,
            "date": str(self.date),
        }




class Ok(BaseModel):
    ok: str = "Ok"

    
class Error(BaseModel):
    error: str = Field(description="Error message")