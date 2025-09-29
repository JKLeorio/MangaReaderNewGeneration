import logging
import uuid
from pathlib import Path
from fastapi import UploadFile
import aiofiles

from settings import MEDIA, ROOT, SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)


async def upload_file(file: UploadFile) -> str:
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    # file_url = str((MEDIA / filename).resolve())
    file_url = str(Path(MEDIA) / Path(filename).resolve())
    extension = filename.split('.')[-1]
    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        async with aiofiles.open(file_url, mode="wb") as new_file:
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


