from typing import Any
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from fastapi_filter.contrib.sqlalchemy import Filter

from models.comic import Chapter, Comic
from models.person import Person
from schemas.comic import ComicCreate, ComicResponse, ComicsPaginated
from schemas.pagination import Pagination
from utils.validators import validate_ids
from ..base_service import BaseService
from utils.media_client import upload_file, delete_file


class ComicService(BaseService):
    model = Comic
    fk_fields_on_create = {
        Person : ['artist_id', 'author_id']
    }
    fk_fields_on_update = {
        Person : ['artist_id', 'author_id']
    }
    async def create(
        self,
        create_data: ComicCreate,
        cover_img: UploadFile
    ) -> Comic:
        # validated_data = ComicCreate.model_validate(create_data, from_attributes=True)

        # await validate_ids(
        #         session=self._session,
        #         models_ids={
        #             Person: [
        #                 create_data.artist_id,
        #                 create_data.author_id
        #                 ],
        #             }
        #     )
        await self.validate_ids(
            create_data,
            self.fk_fields_on_create
        )
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
            await self._session.flush()
            return new_comic
        except Exception as error:
            delete_file(cover_url)
            raise

    async def get_paginated_comics(
        self,
        pagination: Pagination,
        filter: Filter
    ) -> ComicsPaginated:
        paginated_comics = await self.get_paginated(
        filter=filter,
        limit=pagination.size,
        page=pagination.page,
        options=[
            joinedload(Comic.artist),
            joinedload(Comic.author),
            selectinload(Comic.genres)
            ]
        )
        comics = paginated_comics.get('items')
        pagination_status = paginated_comics.get('pagination')
        response = ComicsPaginated(
            comics=[
                ComicResponse.model_validate(
                    comic,
                    from_attributes=True
                ) for comic in comics
            ],
            pagination=pagination_status
        )
        return response

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
    
    async def update(self, scalar, update):
        return await super().update(scalar, update)