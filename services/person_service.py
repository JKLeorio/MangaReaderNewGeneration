
from pydantic import BaseModel
from sqlalchemy import select

from models.person import Person

from .base_service import BaseService

class PersonService(BaseService):
    model = Person

    async def create(
        self,
        person_data: BaseModel
    ) -> Person:
        person_data_dumped = person_data.model_dump()
        new_person = Person(**person_data_dumped)
        self._session.add(new_person)
        self._session.flush()
        return new_person
    
