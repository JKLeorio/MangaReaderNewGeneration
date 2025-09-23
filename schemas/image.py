from typing import Optional
from pydantic import BaseModel

from schemas.user import UserBase

class ImageBase(BaseModel):
    id: int
    url: str
    filename: str
    extension: str
    uploaded_by_id: int



class ImageResponse(BaseModel):
    id: int
    url: str
    filename: str
    extension: str
    uploaded_by: UserBase


class ImageCreate(BaseModel):
    url: str
    filename: str
    extension: str


class ImagePartialUpdate(BaseModel):
    url: Optional[str] = None
    filename: Optional[str] = None
    extension: Optional[str] = None

