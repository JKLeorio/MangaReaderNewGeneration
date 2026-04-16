from pydantic import BaseModel, ConfigDict

from db.types import UserLIbraryItemStatus


class UserLibraryItemBase(BaseModel):
    comic_id: int
    user_id: int
    type: UserLIbraryItemStatus


class UserLibraryItemCreate(BaseModel):
    comic_id: int
    type: UserLIbraryItemStatus