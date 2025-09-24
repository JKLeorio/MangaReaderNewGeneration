from typing import Optional
from pydantic import BaseModel


class CoverBase(BaseModel):
    id: int
    position: int
    image_id: int


class CoverResponse(BaseModel):
    id: int
    position: int
    image_url: str


class CoverCreate(BaseModel):
    position: int
    image_id: int


class CoverBase(BaseModel):
    position: Optional[int] = None
    image_id: Optional[int] = None