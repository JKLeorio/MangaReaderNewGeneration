from datetime import date
from sqlalchemy import Date, ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

import urllib

from settings import MEDIA_URL
from .base import Base, FileMixin

# if TYPE_CHECKING:
#     from .comic import Comic
#     from .image import Image

from .comic import Comic
# from .image import Image



class Person(FileMixin, Base):
    __tablename__ = "persons"
    file_field="avatar_url"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
        )
    full_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    avatar_url: Mapped[str] = mapped_column(
        String,
        default=urllib.parse.urljoin(MEDIA_URL, "default_avatar.jpg"),
        nullable=True
    )
    # avatar_id: Mapped[int] = mapped_column(
    #     ForeignKey("images.id", ondelete="SET NULL"),
    #     nullable=True
    # )
    # avatar: Mapped["Image"] = relationship(
    #     "Image",
    #     passive_deletes=True
    # )
    comics_author: Mapped[list["Comic"]] = relationship(
        "Comic",
        back_populates="author",
        foreign_keys="Comic.author_id",
        passive_deletes=True
    )
    comics_artist: Mapped[list["Comic"]] = relationship(
        "Comic",
        foreign_keys="Comic.artist_id",
        back_populates="artist",
        passive_deletes=True
    )
    # @property
    # def avatar_url(self) -> str:
    #     if self.avatar is not None:
    #         return self.avatar.url
    #     return None

