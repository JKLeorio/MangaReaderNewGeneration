from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from api.auth.depends import current_user
from models.user import User
from schemas.user_library_item import UserLibraryItemResponse, UserLibraryItemCreate, UserLibraryItemPartialUpdate
from services.comic.user_library_service import UserLibraryService


user_library_router = APIRouter()


@user_library_router.get(
        '/',
        response_model=List[UserLibraryItemResponse],
        status_code=status.HTTP_200_OK
)
async def get_current_user_library(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_library_service = UserLibraryService(
        session=session
    )
    user_library = await user_library_service.get_user_library(
        user_id=user.id
    )
    return user_library


@user_library_router.get(
        '/user/{user_id}',
        response_model=List[UserLibraryItemResponse],
        status_code=status.HTTP_200_OK
)
async def get_user_library(
    user_id: int,
    # user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_library_service = UserLibraryService(
        session=session
    )
    user_library = await user_library_service.get_user_library(
        user_id=user_id
    )
    return user_library




@user_library_router.post(
    '/',
    response_model=UserLibraryItemResponse,
    status_code=status.HTTP_200_OK
)
async def add_comic_to_user_library(
    create_data: UserLibraryItemCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user_library_service = UserLibraryService(
        session=session
    )
    new_user_library_item = await user_library_service.create(
        user=user,
        create_data=create_data
    )
    await user_library_service.commit()
    return new_user_library_item
    


@user_library_router.patch(
    '/{comic_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserLibraryItemResponse
)
async def update_user_library_item(
    comic_id: int,
    update_data: UserLibraryItemPartialUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_library_service = UserLibraryService(
        session=session
    )
    user_library_item_updated = await user_library_service.update_by_comic_id(
        comic_id=comic_id,
        user_id=user.id,
        update_data=update_data
    )
    await user_library_service.commit()
    return user_library_item_updated

@user_library_router.delete(
    '/{comic_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_user_library_item(
    comic_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_library_service = UserLibraryService(
        session=session
    )
    await user_library_service.delete_by_comic_id(
        comic_id = comic_id,
        user_id = user.id
    )
    await user_library_service.commit()
    return

