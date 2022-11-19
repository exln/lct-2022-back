from datetime import datetime
from typing import List
import uuid
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import Enum


class MetroSchema(BaseModel):
    id: int
    name = str

    line_id = int

    latitude = str
    longitude = str

    created_at: datetime
    updated_at: datetime


# User Schemas
class UserBaseSchema(BaseModel):
    name: constr(min_length=2)
    last_name: constr(min_length=2)
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: str = 'user'


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: uuid.UUID


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


# UsersRequests Schemas
class UserRequestBaseSchema(BaseModel):
    user_id: uuid.UUID | None = None
    status: bool = 'False'
    name: str
    size: int

    class Config:
        orm_mode = True


class UserRequestResponse(UserRequestBaseSchema):
    id: uuid.UUID
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UserRequestCreate(UserRequestBaseSchema):
    pass


class UserRequestUpdate(BaseModel):
    user_id: uuid.UUID | None = None
    status: bool | None = None

    class Config:
        orm_mode = True


class UserRequestList(BaseModel):
    status: str
    results: int
    users_requests: List[UserRequestResponse]


# Flats Schemas
class Segment(str, Enum):
    NEW = "NEW"
    MODERN = "MODERN"
    OLD = "OLD"


class Material(str, Enum):
    BRICK = "BRICK"
    PANEL = "PANEL"
    MONO = "MONO"


class Renovation(str, Enum):
    WITHOUT = "WITHOUT"
    MUNICIP = "MUNICIP"
    WITHNEW = "WITHNEW"

# class Flat(BaseModel):
#     id = uuid.UUID

#     request_id: uuid.UUID
#     standard: bool

#     latitude: str
#     longitude: str
#     location: str

#     setting = str
#     area = float
#     object_type = str
#     floor = int
#     floors = int
#     metro_id = int
#     metro_remoteness = int
#     rooms = int
#     material = Material
#     segment = Segment
#     kitchen = float
#     balcony = bool
#     renovation = Renovation
#     additions = str
#     price = float
#     price_per_metre = float

#     created_at = datetime
#     updated_at = datetime


class FlatSchema(BaseModel):

    id: int

    location: str

    area: float
    floor: int
    floors: int
    metro_remoteness: int
    rooms: str
    material: str
    segment: str
    kitchen: float
    balcony: str
    renovation: str

    class Config:
	    orm_mode=True
