from typing import Any, TypeVar
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload


from models.comic import Chapter, Comic
from schemas.comic import ChapterCreate
from ..base_service import BaseService

class ChapterService(BaseService):
    model = Chapter

    fk_fields_on_create = {
        Comic : ["comic_id"]
    }
    fk_fields_on_update = {
        Comic : ["comic_id"]
    }

    async def create(
        self,
        create_data: ChapterCreate,
    ) -> Chapter:
        new_chapter = Chapter(**create_data.model_dump())
        self._session.add(new_chapter)
        await self._session.flush()
        return new_chapter

    async def get_chapter_with_pages(
        self,
        chapter_id: int
    ):
        stmt = (
            select(Chapter)
            .options(
                joinedload(Chapter.pages)
            )
            .where(Chapter.id == chapter_id)
        )
        result = await self._session.execute(stmt)
        chapter = result.scalar_one_or_none()
        if chapter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="chapter not found"
            )
        return chapter
    