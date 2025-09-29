import logging
import os
import sys
from pathlib import Path
from fastapi import UploadFile
import aiofiles

from settings import MEDIA, ROOT, SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)


async def upload_file(file: UploadFile) -> str:
    filename = file.filename
    file_url = MEDIA / "filename"
    extension = filename.split('.')[-1]
    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        with aiofiles.open(file_url, mode="wb") as new_file:
            while chunk := await file.read(1024):
                await new_file.write(chunk)
    return file_url



def delete_file(file_url: str):
    try:
        current_file = Path(file_url)
        if current_file.exists():
            current_file.unlink()
    except Exception as error:
        logger.error(error)
