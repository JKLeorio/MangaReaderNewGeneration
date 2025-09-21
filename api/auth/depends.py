from fastapi import Depends, HTTPException, status
from typing import Annotated, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession

from .auth import oauth2_scheme
from models.user import User
from services.user_service import UserService
from utils.jwt import validate_jwt
from db.database import get_async_session


async def current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_async_session)
        ) -> Awaitable[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = validate_jwt(token=token)
    if payload is None:
        raise credentials_exception
    user_id = payload.id
    user_service = UserService(session=session)
    user = await user_service.get_user(User.id == user_id)
    if user is None:
        raise credentials_exception
    if (user.login != payload.login) and (user.email != payload.email):
        raise credentials_exception
    return user


