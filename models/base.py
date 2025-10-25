from sqlalchemy import event
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from utils.media_client import delete_file


class Base(DeclarativeBase, AsyncAttrs):
    pass


class FileMixin:
    file_field: str = "file_field"

    @classmethod
    def __declare_last__(cls):
        @event.listens_for(cls, "after_delete")
        def _delete_file_(mapper, connection, target):
            file_url = getattr(target, cls.file_field, None)
            delete_file(file_url)