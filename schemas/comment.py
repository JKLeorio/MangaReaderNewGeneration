from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from db.types import CommentRefers
from schemas.user import UserBase


class CommentBase(BaseModel):
    id: int
    content: str
    refers_to: CommentRefers
    record_id: int
    parent_id: Optional[int] = None
    depth: int
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class CommentResponse(BaseModel):
    id: int
    content: str
    refers_to: CommentRefers
    record_id: int
    parent_id: Optional[int] = None
    depth: int
    created_at: datetime
    owner: UserBase
    childrens: Optional[List['CommentResponse']] = None

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str
    record_id: int
    refers_to: CommentRefers
    # owner_id: int
    parent_id: Optional[int] = None

class CommentPartialUpdate(BaseModel):
    content: Optional[str] = None
