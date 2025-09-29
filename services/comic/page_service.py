

from fastapi import UploadFile
from pydantic import BaseModel
from models.comic import Page
from utils.media_client import delete_file, upload_file
from ..base_service import BaseService


class PageService(BaseService):
    model = Page

    async def create(
        self,
        page_img: UploadFile,
        page_create: BaseModel
    ) -> Page:
        page_url = await upload_file(page_img)
        try:
            new_page = Page(
                **page_create.model_dump(),
                image_url=page_url
                )
            await self._session.add(new_page)
            await self.commit
        except Exception as error:
            delete_file(page_url)
            raise
        return new_page