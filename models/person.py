from datetime import date
from sqlalchemy import Date, ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .comic import Comic
    from .image import Image


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
        )
    full_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    avatar_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True
    )
    avatar: Mapped["Image"] = relationship(
        "Image",
        passive_deletes=True
    )
    comics_author: Mapped["Comic"] = relationship(
        "Comic",
        back_populates="author",
        passive_deletes=True
    )
    comics_artist: Mapped["Comic"] = relationship(
        "Comic",
        back_populates="artist",
        passive_deletes=True
    )
    @property
    def avatar_url(self) -> str:
        return self.avatar.url

