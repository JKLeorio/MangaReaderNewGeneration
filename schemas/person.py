from datetime import date
from typing import Optional
from pydantic import BaseModel

# from schemas.image import ImageBase

class PersonBase(BaseModel):
    id: int
    full_name: str
    description: str
    birth_date: date
    avatar_id: int

class PersonResponse(BaseModel):
    id: int
    full_name: str
    description: str
    birth_date: date
    # avatar: ImageBase
    avatar_url: str


class PersonCreate(BaseModel):
    full_name: str
    description: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_id: int
    
    