
import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from settings import MEDIA_FOLDER, SUPPORTED_IMAGE_EXTENSIONS

media_router = APIRouter()


@media_router.get(
    "/{image_path}",
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
    image_path: str
):
    if image_path and os.path.exists(image_path):
        file_extension = image_path.split(".")[-1]
        if file_extension in SUPPORTED_IMAGE_EXTENSIONS:
            full_image_path = MEDIA_FOLDER / image_path
            return FileResponse(
                path=full_image_path,
                media_type=f"image/{file_extension}"
                )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="image not found"
    )