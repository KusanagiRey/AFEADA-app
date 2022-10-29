from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AddressSchema(BaseModel):
    id: Optional[int]
    street: str
    house_number: str
    flat: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class DCPSchema(BaseModel):
    id: Optional[int]
    amount: int

    class Config:
        orm_mode = True


class RoleSchema(BaseModel):
    id: Optional[int]
    role: str

    class Config:
        orm_mode = True


class CharacteristicSchema(BaseModel):
    id: Optional[int]
    Strength: Optional[int]
    Agility: Optional[int]
    Flexibility: Optional[int]
    Stamina: Optional[int]
    Stress_resist: Optional[int]

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: Optional[int]
    login: str
    password: str
    surename: str
    name: str
    patronymic: Optional[str]
    id_address: int
    phone: str
    id_dcp: Optional[int]
    id_role: int
    id_characteristic: Optional[int]

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    id: Optional[int]
    name: str
    id_teacher: int

    class Config:
        orm_mode = True


class NewsSchema(BaseModel):
    id: Optional[int]
    news_title: str
    news_description: Optional[str]
    id_autor: int

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: Optional[int]
    event_title: str
    event_description: Optional[str]
    event_date: datetime
    id_autor: int

    class Config:
        orm_mode = True


class TimetableSchema(BaseModel):
    id: Optional[int]
    id_group: int
    id_event: int

    class Config:
        orm_mode = True


class TimetableList(BaseModel):
    count: int
    timetab: List[TimetableSchema]
