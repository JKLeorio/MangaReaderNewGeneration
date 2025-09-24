from typing import Annotated
from fastapi import APIRouter, UploadFile, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from models.image import Image
from schemas.image import ImageBase, ImageResponse

image_router = APIRouter()


image_router.get(
    "/images",
    response_model=ImageBase,
    status_code=status.HTTP_200_OK
)
async def get_images(
    session: AsyncSession
):
    pass

image_router.get(
    "/{image_id}",
    response_model=ImageBase,
    status_code=status.HTTP_200_OK
)
async def get_image(
    image_id: int,
    session: AsyncSession
):
    pass

image_router.post(
    "/",
    response_model=ImageBase,
    status_code=status.HTTP_200_OK
)
async def upload_image(
    image: UploadFile,
    session: AsyncSession
):
    image


image_router.patch(
    "/",
    response_model=ImageBase,
    status_code=status.HTTP_200_OK
)
async def update_image(
    image_id: int,
    session: AsyncSession
):
    pass

image_router.delete(
    "/{image_id}",
    response_model=ImageBase,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_image(
    image_id: int,
    session: AsyncSession
):
    pass

