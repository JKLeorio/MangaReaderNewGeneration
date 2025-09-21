from fastapi import (
    Depends, 
    APIRouter, 
    status
    )
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth import TokenResponse
from db.database import get_async_session
from schemas.auth.payload import PayloadBase
from schemas.auth.register import UserRegister
from services.user_service import UserService
from utils.jwt import generate_jwt
from utils.datetime_utils import get_current_time
from settings import TOKEN_LIFETIME

register_router = APIRouter()


@register_router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    register_data: UserRegister,
    session: AsyncSession = Depends(get_async_session),
):
    now = get_current_time()
    user_service = UserService(session=session)
    new_user = await user_service.create_user(user_data=register_data)
    await user_service.commit()
    await user_service.refresh_user(new_user)
    payload = PayloadBase(
        id = new_user.id,
        username = new_user.username,
        email = new_user.email,
        expire_at = now + TOKEN_LIFETIME
    ).model_dump()
    token = generate_jwt(payload=payload)
    response = TokenResponse(
        access_token=token
    )
    return response
