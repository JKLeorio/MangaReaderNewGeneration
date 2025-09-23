from models.comic import Comic
from .base_service import BaseService


class ComicService(BaseService):
    
    async def create(
        self,
        create_data,
    ) -> Comic:
        pass