from typing import Annotated
from fastapi import APIRouter, status, Depends

from api.auth.depends import current_user
from models.user import User

from ..auth.auth import oauth2_scheme

comic_router = APIRouter()

@comic_router.get(
    "/comics",
    status_code=status.HTTP_200_OK
)
async def get_comics(
    user: User = Depends(current_user)
):
    return {
        "detail": f"Hello"
    }