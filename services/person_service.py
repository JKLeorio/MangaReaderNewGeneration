
from fastapi import UploadFile
from pydantic import BaseModel
from sqlalchemy import select

from models.person import Person
from utils.media_client import delete_file, upload_file

from .base_service import BaseService

class PersonService(BaseService):
    model = Person

    async def create(
        self,
        avatar_img: UploadFile,
        person_data: BaseModel
    ) -> Person:
        avatar_url = await upload_file(avatar_img)
        try:
            person_data_dumped = person_data.model_dump()
            new_person = Person(
                **person_data_dumped,
                avatar_url=avatar_url
                )
            self._session.add(new_person)
            self._session.flush()
        except Exception: 
            delete_file(avatar_url)
            raise
        return new_person
    
