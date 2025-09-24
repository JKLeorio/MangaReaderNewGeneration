from pydantic import BaseModel
from models.comic import Comic
from ..base_service import BaseService


class ComicService(BaseService):
    model = Comic
    
    async def create(
        self,
        create_data: BaseModel,
    ) -> Comic:
        pass