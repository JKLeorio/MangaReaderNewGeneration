from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Sequence, TypeVar

from sqlalchemy import select

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
    

    async def get(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        throw_exception: bool = False,
    ) -> T | None:
        stmt = (
            select(self.model)
            .where(
                *conditions
                )
            .options(*options,)
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
    ) -> Sequence[T]:
        stmt = (
            select(self.model)
            .where(
                *conditions
            )
            .options(
                *options
                )
            )
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return users


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