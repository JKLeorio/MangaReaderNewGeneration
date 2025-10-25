from typing import List
from fastapi import APIRouter, Form, UploadFile, status, Depends
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from api.auth.depends import current_user
from db.database import get_async_session
from models.comic import Chapter, Comic
from schemas.comic import ChapterResponse, ComicCreate, ComicFilter, ComicPartialUpdate, ComicResponse
from services.comic.chapter_service import ChapterService
from services.comic.comic_service import ComicService
from utils.validators import validate_ids
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
        filter=filter,
        options=[
            joinedload(Comic.artist),
            joinedload(Comic.author),
            selectinload(Comic.genres)
        ]
    )
    response = [
        ComicResponse.model_validate(
            comic,
            from_attributes=True
        ) for comic in comics
    ]
    return response

@comic_router.get(
    "/{comic_id}/chapters",
    response_model=List[ChapterResponse],
    status_code=status.HTTP_200_OK
)
async def get_comic_chapters(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    await validate_ids(
        session=session,
        models_ids={
            Comic: [comic_id]
        }
    )
    chapter_service = ChapterService(session=session)
    chapters = await chapter_service.get_all(
        Chapter.comic_id == comic_id,
    )
    response = [
        ChapterResponse.model_validate(
            chapter,
            from_attributes=True
        ) for chapter in chapters
    ]
    return response


@comic_router.post(
    "/",
    response_model=ComicResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comic(
    cover_img: UploadFile,
    comic_create: ComicCreate = Depends(ComicCreate.as_form),
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    comic_service = ComicService(session=session)
    new_comic = await comic_service.create(
        create_data=comic_create, 
        cover_img=cover_img
        )
    await comic_service.commit()
    await comic_service.refresh(
        new_comic,
        attribute_names=["artist","author", "genres"]
    )
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
    await comic_service.commit()
    await comic_service.refresh(
        comic,
        attribute_names=["artist","author", "genres"]
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
    await comic_service.delete_by_id(
        id=comic_id
    )
    await comic_service.commit()
    return 
