from typing import (
    Any,
    Awaitable,
    Dict,
    Sequence
)

from fastapi import HTTPException, status
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate

from services.utils import conditions_generator
from utils.security import generate_hashed_password

class UserService:
    """
    async service
    Contains all user business logic

    all methods that writes in database use session 'flush' method
    you must call built in 'commit' method after finish you logic
    """

    _session: AsyncSession = None
    _in_load_attributes: Sequence[str] = None

    def __init__(
        self,
        session: AsyncSession,
        in_load_attributes: Sequence[str] = None
    ):
        self._session = session
        self._in_load_attributes = in_load_attributes

    async def is_unique(
        self,
        user_update: BaseModel
    ):
        user_dump = user_update.model_dump()
        fields = dict()
        fields["username"] = user_dump.pop("username")
        fields["email"] = user_dump.pop("email")
        conditions = conditions_generator(User, filters=fields)
        stmt = (
            select(User)
            .where(
                *conditions
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar() is None
    
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

    async def refresh_user(
            self,
            user: User,
    ):
        await self._session.refresh(
            user,
            attribute_names=self._in_load_attributes
        )


    async def create_user(
        self,
        user_data: BaseModel
    ) -> User:
        if not self.is_unique(user_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user already exists"
                )
        user_dump = user_data.model_dump(exclude_unset=True)
        password = user_dump.pop("password")
        hashed_password = generate_hashed_password(password=password)
        user_data_validated = UserCreate(
            **user_dump, 
            hashed_password=hashed_password
            )
        new_user = User(**user_data_validated.model_dump())
        self._session.add(new_user)
        await self._session.flush()
        return new_user
    

    async def get_user(
        self,
        # user_id: int,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
        throw_exception: bool = False,
        # **filters
    ) -> User | None:
        # conditions = conditions_generator(User, filters=filters)
        stmt = (
            select(User)
            .where(
                # User.id == user_id,
                *conditions
                )
            .options(*options)
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if (throw_exception is True) and (user is None):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user not found"
                )
        return user

    async def get_users(
        self,
        session: AsyncSession,
        *conditions: Sequence[Any],
        options: Sequence[Any] = [],
    ) -> Sequence[User]:
        stmt = (
            select(User)
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


    async def update_user_by_id(
        self,
        user_id: int,
        user_update: Dict
    ) -> User:
        user = await self.get_user(
            User.id==user_id,
            throw_exception=True
        )
        updated_user = await self.update_user(
            user=user,
            user_update=user_update,
            session=self._session
        )
        return updated_user


    async def update_user(
        self,
        user: User,
        user_update: Dict
        ) -> User:
        for key, value in user_update.items():
            setattr(user, key, value)
        await self._session.flush()
        return user


    async def get_user_by_email(
        self,
        email: str,
        ) -> User | None:
        user = await self.get_user(
            User.email == email,
            throw_exception=True
        )
        return user 
    
    
    async def is_user_exist(
        self,
        session: AsyncSession, 
        email: str
        ) -> bool:
        user = await self.get_user_by_email(email=email)
        return user is None