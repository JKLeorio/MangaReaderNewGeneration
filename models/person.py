from datetime import date
from sqlalchemy import Date, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .comic import Comic


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        autoincrement=True
        )
    full_name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)

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
