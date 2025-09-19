from datetime import date
from typing import Optional
from pydantic import BaseModel


class UserShort(BaseModel):
    id: int
    first_name: str
    last_name: str
    login:str

class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    login: str
    email: str
    birth_date: date


class UserResponse(UserBase):
    pass


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    login: str
    email: str
    password: str
    birth_date: Optional[date] = None

