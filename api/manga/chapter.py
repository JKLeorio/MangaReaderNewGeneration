from typing import Annotated, List, Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from api.auth.depends import current_user
from db.database import get_async_session
from models.comic import Chapter
from schemas.comic import ChapterCreate, ChapterPartialUpdate, ChapterResponse
from services.comic.chapter_service import ChapterService
from ..auth.auth import oauth2_scheme


chapter_router = APIRouter()


@chapter_router.get(
    "/{comic_id}/chapters",
    response_model=List[ChapterResponse],
    status_code=status.HTTP_200_OK
)
async def get_comic_chapters(
    comic_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
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


@chapter_router.get(
    "/chapters/{chapter_id}",
    response_model=List[ChapterResponse],
    status_code=status.HTTP_200_OK
)
async def get_chapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    chapter_service = ChapterService(session=session)
    chapter = chapter_service.get(
        Chapter.id == chapter_id,
        throw_exception=True
        )
    response = ChapterResponse.model_validate(chapter, from_attributes=True)
    return response

@chapter_router.post(
    "/{comic_id}",
    response_model=ChapterResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_chapter(
    comic_id: int,
    chapter_create: ChapterCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    chapter_service = ChapterService(session=session)
    new_chapter = await chapter_service.create(create_data=chapter_create)
    return ChapterResponse.model_validate(new_chapter, from_attributes=True)

@chapter_router.patch(
    "/{chapter_id}",
    response_model=ChapterResponse,
    status_code=status.HTTP_200_OK
)
async def update_chapter(
    chapter_id: int,
    chapter_update: ChapterPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    chapter_service = ChapterService(session=session)
    chapter = await chapter_service.update_by_id(
        id=chapter_id,
        update=chapter_update
        )
    return ChapterResponse.model_validate(chapter, from_attributes=True)
    


@chapter_router.delete(
    "/{chapter_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_chapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    chapter_service = ChapterService(session=session)
    await chapter_service.delete(
        chapter_id=chapter_id
    )
    return 