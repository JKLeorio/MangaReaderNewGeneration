import logging
import uuid
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import urllib.parse

from settings import MEDIA, MEDIA_FOLDER, MEDIA_FOLDER_LOCATION, MEDIA_URL, ROOT, SUPPORTED_IMAGE_EXTENSIONS

logger = logging.getLogger(__name__)


async def upload_file(file: UploadFile) -> str:
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    # file_url = str((MEDIA / filename).resolve())
    file_url = urllib.parse.urljoin(MEDIA_URL, filename)
    file_location = Path(MEDIA_FOLDER) / filename
    extension = filename.split('.')[-1]
    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        async with aiofiles.open(file_location, mode="wb") as new_file:
            while chunk := await file.read(1024):
                await new_file.write(chunk)
    return file_url


def delete_file(file_url: str):
    try:
        parsed_url = urllib.parse.urlparse(file_url)
        relative_file_location = Path(parsed_url.path.lstrip('/\\'))
        full_file_location = Path(MEDIA_FOLDER_LOCATION) / relative_file_location
        logger.warning(full_file_location)
        if full_file_location.exists():
            logger.warning(full_file_location)
            full_file_location.unlink()
    except Exception as error:
        logger.error(error)


