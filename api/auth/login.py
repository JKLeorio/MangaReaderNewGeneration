from typing import Annotated, Awaitable
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from models.user import User
from schemas.auth.login import UserLogin
from schemas.auth.payload import PayloadBase
from services.user_service import UserService
from settings import TOKEN_LIFETIME
from utils.datetime_utils import get_current_time
from utils.jwt import generate_jwt
from utils.security import validate_password
from .auth import TokenResponse

auth_router = APIRouter()


async def login_base(
    login: str,
    password: str,
    session: AsyncSession
) -> Awaitable[str]:
    now = get_current_time()
    user_service = UserService(session=session)
    user: User = await user_service.get_user(
        login=login,
        throw_exception=True
    )
    if not validate_password(
        hashed_password=user.hashed_password, 
        password=password
        ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            #Заменить к концу проекта
            detail="incorrect password"
        )
    payload = PayloadBase(
        id = user.id,
        login = user.login,
        email = user.email,
        expire_at = now + TOKEN_LIFETIME
    ).model_dump()
    token = generate_jwt(payload=payload)
    return token


@auth_router.get(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
    )
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session),
):
    login = login_data.login
    password = login_data.password
    token = await login_base(
        login=login,
        password=password,
        session=session
    )
    response = TokenResponse(access_token=token)
    return response


@auth_router.get(
    "/form_login",
    status_code=status.HTTP_200_OK
    )
async def login_with_form(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    login = login_data.username
    password = login_data.password
    token = await login_base(
        login=login,
        password=password,
        session=session
    )
    response = {
        "access_token": token,
        "token_type": "bearer"
    }
    return response