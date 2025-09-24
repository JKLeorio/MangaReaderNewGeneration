from typing import Annotated, List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.depends import current_user
from db.database import get_async_session
from models.user import User
from schemas.comic import ComicCreate, ComicResponse

from ..auth.auth import oauth2_scheme

comic_router = APIRouter()

@comic_router.get(
    "/comics",
    response_model=List[ComicResponse],
    status_code=status.HTTP_200_OK
)
async def get_comics(
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    return {
        "detail": f"Hello"
    }

@comic_router.post(
    "/",
    response_model=ComicResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comic(
    comic_data: ComicCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    pass


@comic_router.patch(
    "/{comic_id}",
    response_model=ComicResponse,
    status_code=status.HTTP_200_OK
)
async def update_comic(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    return {
        "detail": f"Hello"
    }


@comic_router.delete(
    "/{comic_id}",
    response_model=ComicResponse,
    status_code=status.HTTP_200_OK
)
async def delete_comic(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    return {
        "detail": f"Hello"
    }