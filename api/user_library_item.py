from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from auth.depends import current_user
from db.types import UserLIbraryItemStatus
from models.user import User
from schemas.user_library_item import UserLibraryItemBase, UserLibraryItemCreate
from services.comic.user_library_item_service import UserLibraryItemService


user_library_item_router = APIRouter()


@user_library_item_router.get(
    '/',
    response_model=UserLibraryItemBase,
    status_code=status.HTTP_200_OK
)
async def get_user_library(
    create_data: UserLibraryItemCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_library_item_service = UserLibraryItemService(
        session=session
    )
    new_user_library_item = await user_library_item_service.create(
        user=user,
        create_data=create_data
    )
    

