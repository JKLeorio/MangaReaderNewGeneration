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
    username: str,
    password: str,
    session: AsyncSession
) -> Awaitable[str]:
    now = get_current_time()
    incorrect_data_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_service = UserService(session=session)
    user: User = await user_service.get_user(
        User.username == username,
        throw_exception=False
    )
    if user is None:
        raise incorrect_data_exception
    if not validate_password(
        hashed_password=user.hashed_password, 
        password=password
        ):
        raise incorrect_data_exception
    payload = PayloadBase(
        id = user.id,
        username = user.username,
        email = user.email,
        expire_at = now + TOKEN_LIFETIME
    ).model_dump()
    token = generate_jwt(payload=payload)
    return token


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
    )
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session),
):
    username = login_data.username
    password = login_data.password
    token = await login_base(
        username=username,
        password=password,
        session=session
    )
    response = TokenResponse(access_token=token)
    return response


@auth_router.post(
    "/form_login",
    status_code=status.HTTP_200_OK
    )
async def login_with_form(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    username = login_data.username
    password = login_data.password
    token = await login_base(
        username=username,
        password=password,
        session=session
    )
    response = {
        "access_token": token,
        "token_type": "bearer"
    }
    return response