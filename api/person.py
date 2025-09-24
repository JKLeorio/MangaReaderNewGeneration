from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from models.person import Person
from schemas.person import PersonCreate, PersonResponse, PersonUpdate
from services.person_service import PersonService

person_router = APIRouter()


@person_router.get(
    "/persons",
    response_model=List[PersonResponse],
    status_code=status.HTTP_200_OK
)
async def get_persons(
    session: AsyncSession = Depends(get_async_session),
):
    person_service = PersonService(session=session)
    persons = await person_service.get_all(
        options=[selectinload(Person.avatar)]
    )
    response = [PersonResponse.model_validate(person, from_attributes=True)
                for person in persons]
    return response


@person_router.get(
    "/{person_id}",
    response_model=PersonResponse,
    status_code=status.HTTP_200_OK
)
async def get_persons(
    person_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    person_service = PersonService(session=session)
    person = await person_service.get(
        Person.id == person_id,
        options=[selectinload(Person.avatar)],
        throw_exception=True
    )
    response = PersonResponse.model_validate(person, from_attributes=True)
    return response


@person_router.post(
    "/",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_person(
    create_data: PersonCreate,
    session: AsyncSession = Depends(get_async_session)
):
    person_service = PersonService(session=session)
    new_person = await person_service.create(
        create_data
    )
    await person_service.commit()
    await person_service.refresh(new_person, attribute_names=['avatar'])
    return PersonResponse.model_validate(new_person, from_attributes=True)
    # return PersonResponse(
    #     id=new_person.id,
    #     full_name=new_person.full_name,
    #     birth_date=new_person.birth_date,
    #     description=new_person.description,
    #     avatar_url=new_person.avatar_url
    # )
    


@person_router.patch(
    "/{person_id}",
    response_model=PersonResponse,
    status_code=status.HTTP_200_OK
)
async def update_person(
    person_id: int,
    update_data: PersonUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    person_service = PersonService(
        session=session,
        )
    person = await person_service.get(
        Person.id == person_id,
        throw_exception=True
    )
    update_data_dump = update_data.model_dump(exclude_unset=True)
    updated_person = await person_service.update(
        person,
        update=update_data_dump
    )
    await person_service.commit()
    await person_service.refresh(
        updated_person,
        attribute_names=['avatar']
        )
    return PersonResponse.model_validate(updated_person, from_attributes=True)


@person_router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_person(
    person_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    person_service = PersonService(session=session)
    person = await person_service.get(
        Person.id == person_id,
        throw_exception=True
    )
    await person_service.delete(person)
    await person_service.commit()
    return
