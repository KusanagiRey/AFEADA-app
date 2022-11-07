from typing import Optional, List

from pydantic import BaseModel


class UserSchemaIn(BaseModel):
    id: Optional[int]
    surename: str
    name: str
    patronymic: Optional[str]
    phone: Optional[str]
    dcp: Optional[int]
    role: int

    class Config:
        orm_mode = True

class UserCreateSchema(UserSchemaIn):
    login: str
    password: str

    class Config:
        orm_mode = True

class UserAvatarSchema(BaseModel):
    avatar: str

    class Config:
        orm_mode = True

class СharacteristicSchemaIn(BaseModel):
    id: Optional[int]
    user_id: int
    Strength: Optional[int]
    Agility: Optional[int]
    Flexibility: Optional[int]
    Stamina: Optional[int]
    Stress_resist: Optional[int]

    class Config:
        orm_mode = True

class UserSchemaOut(UserSchemaIn):
    avatar: Optional[str]
    characterisric: Optional[СharacteristicSchemaIn]

    class Config:
        orm_mode = True

class СharacteristicUpdateSchema(BaseModel):
    Strength: Optional[int]
    Agility: Optional[int]
    Flexibility: Optional[int]
    Stamina: Optional[int]
    Stress_resist: Optional[int]


class CardsSchemaIn(BaseModel):
    id: Optional[int]
    card_name: str
    card_discription: str

    class Config:
        orm_mode = True

class CardsSchemaOut(CardsSchemaIn):
    card_look: str

    class Config:
        orm_mode = True

class CardsList(BaseModel):
    count: int
    cards: List[CardsSchemaOut]

class DecksSchema(BaseModel):
    id: Optional[int]
    id_card: int
    id_user: int

    class Config:
        orm_mode = True

class UserDeckSchema(BaseModel):
    card: List[CardsSchemaOut]

    class Config:
        orm_mode = True