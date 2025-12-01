from math import ceil
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Sequence, TypeVar
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Select, func, select

from schemas.pagination import Pagination

T = TypeVar("Model")

class BaseService:
    """
    async service
    Contains all user business logic

    all methods that writes in database use session 'flush' method
    you must call built in 'commit' method after finish you logic
    """

    _session: AsyncSession = None
    _in_load_attributes: Sequence[str] = None
    model: T

    def __init__(
        self,
        session: AsyncSession,
        in_load_attributes: Sequence[str] = None
    ):
        self._session = session
        self._in_load_attributes = in_load_attributes
    
    async def finish(self):
        await self._session.commit()
        await self.close_session()
    
    async def commit(self):
        await self._session.commit()

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

    async def _generate_statement(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        filter: Filter = None,
    ) -> Select[Any]:
        stmt = (
            select(self.model)
            .where(
                *conditions
            )
            .options(
                *options
                )
            )
        if filter is not None:
            stmt = filter.filter(stmt)
        return stmt
        
    

    async def get(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        throw_exception: bool = False,
    ) -> T | None:
        stmt = self._generate_statement(
            conditions,
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
    ) -> Sequence[T]:
        stmt = self._generate_statement(
            conditions,
            options=options,
            filter=filter
        )
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return users
    
    async def get_paginated(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        filter: Filter = None,
        limit: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        stmt = await self._generate_statement(
            *conditions,
            options=options,
            filter=filter
        )
        total_stmt = select(func.count()).select_from(stmt)
        total_result = (await self._session.execute(total_stmt)).scalar_one_or_none()
        stmt.limit(limit=limit)
        result = await self._session.execute(stmt)
        items = result.scalars().all()
        offset = limit * (page-1)
        total = ceil((total_result if total_result else 0) / limit)
        page = total if page > total else page
        response = {
            'items' : items,
            'pagination': Pagination(
                total=total,
                page=page,
                size=limit
            )
        }

        return response

    async def update_by_id(
        self,
        id: int,
        update: Dict
    ) -> T:
        scalar = await self.get(
            self.model.id==id,
            throw_exception=True
        )
        updated_user = await self.update(
            scalar=scalar,
            update=update,
            session=self._session
        )
        return updated_user


    async def update(
        self,
        scalar: T,
        update: Dict
        ) -> T:
        for key, value in update.items():
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
        