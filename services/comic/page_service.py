

from pydantic import BaseModel
from models.comic import Page
from ..base_service import BaseService


class PageService(BaseService):
    model = Page

    async def create(
        page_create: BaseModel
    ) -> Page:
        pass