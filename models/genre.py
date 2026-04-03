import typing

from sqlalchemy import ForeignKey, String, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.association import comic_genre_association_table

if typing.TYPE_CHECKING:
    from models.comic import Comic


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    name: Mapped[str] = mapped_column(
        String
    )
    comics: Mapped[list["Comic"]] = relationship(
        secondary=comic_genre_association_table,
        back_populates="genres"
    )



# class ComicGenre(Base):
#     __tablename__ = "comic_genres"

#     id: Mapped[int] = mapped_column(
#         Integer, primary_key=True, autoincrement=True
#         )
#     comic_id: Mapped[int] = mapped_column(
#         ForeignKey("comics.id", ondelete="CASCADE")
#     )
#     genre_id: Mapped[int] = mapped_column(
#         ForeignKey("genres.id", ondelete="CASCADE")
#     )
