# import os
# import sys

# from models.image import Image
# from fastapi import UploadFile
# from pydantic import BaseModel
# from .base_service import BaseService


# class ImageService(BaseService):
#     model = Image

#     async def create(
#         file: UploadFile,
#         create_data: BaseModel
#     ):
#         pass