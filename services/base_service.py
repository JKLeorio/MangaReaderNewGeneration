from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, Sequence, TypeVar

from sqlalchemy import select

from models.base import Base
from models.user import User
from services.utils import conditions_generator
from utils.security import generate_hashed_password

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
    _model: T

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
    ):
        await self._session.refresh(
            scalar,
            attribute_names=self._in_load_attributes
        )
    

    async def get(
        self,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        throw_exception: bool = False,
    ) -> T | None:
        stmt = (
            select(self._model)
            .where(
                *conditions
                )
            .options(*options)
        )
        result = await self._session.execute(stmt)
        scalar = result.scalar_one_or_none()
        if (throw_exception is True) and (scalar is None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self._model.__name__} not found"
                )
        return scalar

    async def get_all(
        self,
        session: AsyncSession,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
    ) -> Sequence[T]:
        stmt = (
            select(self._model)
            .where(
                *conditions
            )
            .options(
                *options
                )
            )
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users


    async def update_by_id(
        self,
        id: int,
        update: Dict
    ) -> T:
        scalar = await self.get(
            self._model.id==id,
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
        user_update: Dict
        ) -> T:
        for key, value in user_update.items():
            setattr(scalar, key, value)
        await self._session.flush()
        return scalar