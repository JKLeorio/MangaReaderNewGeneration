from typing import Any
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.comic import Chapter, Comic
from schemas.comic import ComicCreate
from ..base_service import BaseService
from utils.media_client import upload_file, delete_file


class ComicService(BaseService):
    model = Comic
    
    async def create(
        self,
        create_data: ComicCreate,
        cover_img: UploadFile
    ) -> Comic:
        # validated_data = ComicCreate.model_validate(create_data, from_attributes=True)

        cover_url = await upload_file(file=cover_img)
        try:
            new_comic = Comic(
                # title=ComicCreateForm.title,
                # type=ComicCreateForm.type,
                # release_date=ComicCreateForm.release_date,
                # author_id=ComicCreateForm.author_id,
                # artist_id=ComicCreateForm.artist_id,
                **create_data.model_dump(),
                cover_url = cover_url,
            )
            self._session.add(new_comic)
            await self.commit()
            await self.refresh(new_comic)
            return new_comic
        except Exception as error:
            delete_file(cover_url)
            raise

    async def get_comic_with_chapters(
        self,
        *conditions,
        options: list[Any]
    ):
        stmt = (
            select(Comic)
            .options(
                joinedload(Comic.chapters)
            )
            .where()
        )
        result = await self._session.execute(stmt)
        comic = result.scalars().first()
        return comic