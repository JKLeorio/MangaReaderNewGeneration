from typing import Annotated, List, Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from api.auth.depends import current_user
from db.database import get_async_session
from schemas.comic import ComicCreate, ComicFilter, ComicPartialUpdate, ComicResponse
from services.comic.comic_service import ComicService
from ..auth.auth import oauth2_scheme

comic_router = APIRouter()



@comic_router.get(
    "/comics",
    response_model=List[ComicResponse],
    status_code=status.HTTP_200_OK
)
async def get_comics(
    filter: ComicFilter = FilterDepends(ComicFilter),
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    comic_service = ComicService(session=session)
    comics = await comic_service.get_all(
        filter=filter
    )
    response = [
        ComicResponse.model_validate(
            comic,
            from_attributes=True
        ) for comic in comics
    ]
    return response

@comic_router.post(
    "/",
    response_model=ComicResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comic(
    comic_create: ComicCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    comic_service = ComicService(session=session)
    new_comic = await comic_service.create(create_data=comic_create)
    return ComicResponse.model_validate(new_comic, from_attributes=True)

@comic_router.patch(
    "/{comic_id}",
    response_model=ComicResponse,
    status_code=status.HTTP_200_OK
)
async def update_comic(
    comic_id: int,
    comic_update: ComicPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    comic_service = ComicService(session=session)
    comic = await comic_service.update_by_id(
        id=comic_id,
        update=comic_update
        )
    return ComicResponse.model_validate(comic, from_attributes=True)
    


@comic_router.delete(
    "/{comic_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comic(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    comic_service = ComicService(session=session)
    await comic_service.delete(
        comic_id=comic_id
    )
    return 
