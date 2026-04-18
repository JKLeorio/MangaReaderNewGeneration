from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from db.types import UserLIbraryItemStatus
from schemas.pagination import Pagination


class UserLibraryItemBase(BaseModel):
    comic_id: int
    user_id: int


class UserLibraryItemResponse(UserLibraryItemBase):
    type: UserLIbraryItemStatus


class UserLibraryResponse(BaseModel):
    items: Dict[UserLIbraryItemStatus, List[UserLibraryItemBase]]


class UserLibraryPaginatedResponse(UserLibraryResponse):
    pagination: Pagination


class UserLibraryItemCreate(BaseModel):
    comic_id: int
    type: UserLIbraryItemStatus


class UserLibraryItemPartialUpdate(BaseModel):
    type: Optional[UserLIbraryItemStatus] = None
