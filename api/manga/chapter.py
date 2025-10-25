from typing import Annotated, List, Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends
from sqlalchemy.orm import joinedload, selectinload

from api.auth.depends import current_user
from db.database import get_async_session
from models.comic import Chapter
from schemas.comic import ChapterCreate, ChapterPartialUpdate, ChapterResponse, ChapterWithPagesResponse
from services.comic.chapter_service import ChapterService
from ..auth.auth import oauth2_scheme
from .comic import comic_router


chapter_router = APIRouter()


@chapter_router.get(
    "/{chapter_id}",
    response_model=ChapterWithPagesResponse,
    status_code=status.HTTP_200_OK
)
async def get_chapter_with_pages(
    chapter_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    chapter_service = ChapterService(session=session)
    chapter = await chapter_service.get(
        Chapter.id == chapter_id,
        options=[
            joinedload(Chapter.comic),
            selectinload(Chapter.pages),
            ],
        throw_exception=True
        )
    
    response = ChapterWithPagesResponse.model_validate(chapter, from_attributes=True)
    return response




@chapter_router.post(
    "/",
    response_model=ChapterResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_chapter(
    chapter_create: ChapterCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    chapter_service = ChapterService(session=session)
    new_chapter = await chapter_service.create(create_data=chapter_create)
    await chapter_service.commit()
    await chapter_service.refresh(
        new_chapter, attribute_names=["comic"]
    )
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
    await chapter_service.commit()
    await chapter_service.refresh(
        chapter, attribute_names=["comic"]
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
    await chapter_service.delete_by_id(
        id=chapter_id
    )
    await chapter_service.commit()
    return 