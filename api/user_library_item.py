from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from auth.depends import current_user
from models.user import User


user_library_item_router = APIRouter()


@user_library_item_router.get(
    '',
)
async def get_user_library(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    pass

