from typing import Any, TypeVar
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload


from models.comic import Chapter
from schemas.comic import ChapterCreate
from ..base_service import BaseService

class ChapterService(BaseService):
    model = Chapter

    async def create(
        self,
        chapter_data: ChapterCreate,
    ) -> Chapter:
        new_chapter = Chapter(**ChapterCreate)
        self._session.add(new_chapter)
        await self.commit()
        await self.refresh(new_chapter)
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
    
    async def delete(
        chapter_id: int
    ):
        pass