

from fastapi import UploadFile
from pydantic import BaseModel
from models.comic import Chapter, Page
from utils.media_client import delete_file, upload_file
from ..base_service import BaseService


class PageService(BaseService):
    model = Page
    fk_fields_on_create = {
        Chapter : ["chapter_id"]
    }
    fk_fields_on_update = {
        Chapter : ["chapter_id"]
    }

    async def create(
        self,
        page_img: UploadFile,
        page_create: BaseModel
    ) -> Page:
        await self.validate_ids(
            page_create,
            self.fk_fields_on_create
        )
        page_url = await upload_file(page_img)
        try:
            new_page = Page(
                **page_create.model_dump(),
                image_url=page_url
                )
            await self._session.add(new_page)
            await self._session.flush()
        except Exception as error:
            delete_file(page_url)
            raise
        return new_page