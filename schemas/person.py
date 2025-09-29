from datetime import date
from typing import Annotated, Optional
from fastapi import Form, UploadFile
from pydantic import BaseModel

# from schemas.image import ImageBase

class PersonBase(BaseModel):
    id: int
    full_name: str
    description: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_id: int

class PersonResponse(BaseModel):
    id: int
    full_name: str 
    description: Optional[str] = None
    birth_date: Optional[date] = None
    # avatar: ImageBase
    avatar_url: Optional[str] = None


class PersonCreate(BaseModel):
    full_name: str
    description: Optional[str] = None
    birth_date: Optional[date] = None
    # avatar_id: Optional[int] = None

class PersonCreateForm(BaseModel):
    def __init__(
            self,
            full_name: Annotated[str, Form()],
            description: Annotated[str, Form()] = None,
            avatar: UploadFile = None,
            birth_day: Annotated[date, Form()] = None,
            ):
        self.full_name = full_name
        self.description = description
        self.birth_day = birth_day
        self.avatar = avatar

    
    
class PersonUpdate(BaseModel):
    full_name: Optional[str] = None
    description: Optional[str] = None
    birth_date: Optional[date] = None
    avatar_id: Optional[int] = None