from datetime import date
from typing import Optional
from pydantic import BaseModel

from db.types import Role


class UserShort(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str

class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    birth_date: date
    role: Role


class UserResponse(UserBase):
    pass


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: str
    hashed_password: str
    birth_date: Optional[date] = None
    role: Role = Role.USER

