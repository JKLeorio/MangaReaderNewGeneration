from fastapi import Depends, HTTPException, status
from typing import Annotated, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession

from auth import oauth2_scheme
from models.user import User
from services.user_service import UserService
from utils.jwt import validate_jwt
from db.database import get_async_session


async def current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_async_session)
        ) -> Awaitable[User]:
    payload = validate_jwt(token=token)
    user_id = payload.get("id", None)
    if user_id is None:
        raise HTTPException(
            status=status.HTTP_401_UNAUTHORIZED, 
            detail="unauthorized"
            )
    user_service = UserService(session=session)
    user = user_service.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(
            status=status.HTTP_401_UNAUTHORIZED, 
            detail="unauthorized"
            )
    return user


