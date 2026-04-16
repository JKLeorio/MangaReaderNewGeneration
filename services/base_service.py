from collections import defaultdict
from math import ceil
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Sequence, TypeVar
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Select, func, select
# from sqlalchemy import exc
# from psycopg2.errors import UniqueViolation

from schemas.pagination import Pagination
from utils.validators import validate_ids

T = TypeVar("Model")

class BaseService:
    """
    async service
    Contains all user business logic
    set model that you want to bind with service into 'model' property

    all methods that writes in database use session 'flush' method
    you must call built in 'commit' method after finish you logic
    """

    _session: AsyncSession = None
    _in_load_attributes: Sequence[str] = None
    model: T
    fk_fields_on_create: Dict[T, List[str]] = {}
    fk_fields_on_update: Dict[T, List[str]] = {}

    def __init__(
        self,
        session: AsyncSession,
        in_load_attributes: Sequence[str] = None
    ):
        self._session = session
        self._in_load_attributes = in_load_attributes
    
    async def finish(self):
        if self._session is not None:
            await self._session.commit()
            await self.close_session()
    
    async def commit(self):
        await self._session.commit()
        # try:
        #     await self._session.commit()
        # except exc.IntegrityError as exception:
        #     if isinstance(exception.orig, UniqueViolation):
        #         pass

    async def close_session(self):
        if self._session is not None:
            await self._session.aclose()

    def set_in_load_attributes(
        self,
        in_load_attributes: Sequence[str]
    ):
        self._in_load_attributes = in_load_attributes

    async def refresh(
            self,
            scalar: T,
            attribute_names: Sequence[str] = []
    ):
        await self._session.refresh(
            scalar,
            attribute_names=attribute_names
        )

    def _generate_statement(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        filter: Filter = None,
        order_by: Sequence[Any] = []
    ) -> Select[Any]:
        stmt = (
            select(self.model)
            .where(
                *conditions
            )
            .options(
                *options
                )
            .order_by(
                *order_by
            )
            )
        if filter is not None:
            stmt = filter.filter(stmt)
        return stmt

    async def validate_ids(
            self,
            data_schema: BaseModel,
            fk_fields: Dict[Any, str]
    ):
        try:
            models_ids = dict()
            for model, fields in fk_fields.items():
                models_ids[model] = [
                    getattr(data_schema, field) for field in fields
                ]
        except AttributeError as e:
            e.add_note(
                "check the fields in fk_fields_on_update "
                "and fk_fields_on_create attributes in Service class"
                )
            raise

        await validate_ids(
            self._session,
            models_ids=models_ids
        )

    async def get(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        throw_exception: bool = False,
    ) -> T | None:
        stmt = self._generate_statement(
            *conditions,
            options=options
        )
        result = await self._session.execute(stmt)
        scalar = result.scalar_one_or_none()
        if (throw_exception is True) and (scalar is None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found"
                )
        return scalar
    

    async def get_all(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        filter: Filter = None,
        unique: bool = False,
        order_by: Sequence[Any] = []
    ) -> Sequence[T]:
        stmt = self._generate_statement(
            *conditions,
            options=options,
            filter=filter,
            order_by=order_by
        )
        result = await self._session.execute(stmt)
        if unique is True:
            records = result.unique().scalars().all()
        else:
            records = result.scalars().all()
        return records
    
    async def get_paginated(
        self,
        *conditions: Sequence[Any],
        total_conditions: Sequence[Any] = [],
        total_options: Sequence[Any] = [],
        options: Sequence[Any] = [],
        order_by: Sequence[Any] = [],
        filter: Filter = None,
        limit: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        stmt = self._generate_statement(
            *conditions,
            options=options,
            filter=filter,
            order_by=order_by
        )
        total_stmt = select(func.count()).select_from(stmt)
        if total_conditions:
            total_stmt = select(
                func.count()
            ).select_from(
                self._generate_statement(
                    *conditions,
                    options=options
                )
            )
        total_result = (await self._session.execute(total_stmt)).scalar_one_or_none()
        stmt.limit(limit=limit)
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        offset = limit * (page-1)
        total_pages = ceil((total_result if total_result else 1) / limit)
        page = total_pages if page > total_pages else page
        response = {
            'items' : items,
            'pagination': Pagination(
                total_pages=total_pages,
                page=page,
                size=limit
            )
        }

        return response

    async def update_by_id(
        self,
        id: int,
        update_data: BaseModel,
        options: list[Any] = []
    ) -> T:
        scalar = await self.get(
            self.model.id==id,
            throw_exception=True,
            options=options
        )
        updated_user = await self.update(
            scalar=scalar,
            update_data=update_data
        )
        return updated_user


    async def update(
        self,
        scalar: T,
        update_data: BaseModel
        ) -> T:
        await self.validate_ids(
            update_data,
            self.fk_fields_on_update
        )
        update_dump = update_data.model_dump(exclude_none=True)
        for key, value in update_dump.items():
            setattr(scalar, key, value)
        await self._session.flush()
        return scalar
    
    async def delete(
        self,
        scalar: T,
    ) -> bool:
        try:
            await self._session.delete(scalar)
            await self._session.flush()
            return True
        except Exception as error:
            raise f"Error in delete object of type {type(scalar)} \n" \
                    "error is :{error}"
        
    async def delete_by_id(
        self,
        id: int,
    ):
        scalar = await self.get(
            self.model.id == id,
            throw_exception=True
        )
        await self.delete(scalar=scalar)
        