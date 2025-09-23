from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.comic import PageBase
from schemas.user import UserBase


class CommentBase(BaseModel):
    id: int
    page_id: int
    content: str
    created_at: datetime
    owner_id: int

class CommentResponse(BaseModel):
    id: int
    content: str
    page: PageBase
    created_at: datetime
    owner: UserBase
    childrens: 'Optional[CommentResponse]' = None

class CommentCreate(BaseModel):
    content: str
    page_id: int
    # owner_id: int

class CommentPartialUpdate(BaseModel):
    content: Optional[str] = None