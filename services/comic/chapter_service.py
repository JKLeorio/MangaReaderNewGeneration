

from pydantic import BaseModel
from models.comic import Chapter
from ..base_service import BaseService


class ChapterService(BaseService):
    model = Chapter

    async def create(
        chapter_data: BaseModel
    ) -> Chapter:
        pass