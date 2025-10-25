
import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from settings import MEDIA_FOLDER, SUPPORTED_IMAGE_EXTENSIONS

media_router = APIRouter()


@media_router.get(
    "/{image_name}",
    responses={
          200: {
            "content": {
                    "image/png" : {"schema": {"type":"string", "format":"binary"}},
                    "image/jpeg": {"schema": {"type": "string", "format": "binary"}},
                    "image/webp": {"schema": {"type": "string", "format": "binary"}},
                }
          }
    }
)
async def get_image(
    image_name: str
):
    if image_name:
        full_image_path = MEDIA_FOLDER / image_name
        if os.path.exists(full_image_path):
            file_extension = image_name.split(".")[-1]
            if file_extension in SUPPORTED_IMAGE_EXTENSIONS:
                return FileResponse(
                    path=full_image_path,
                    media_type=f"image/{file_extension}"
                    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="image not found"
    )