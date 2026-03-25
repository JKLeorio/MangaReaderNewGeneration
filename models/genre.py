from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base 


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    name: Mapped[str] = mapped_column(
        String
    )
    comics: Mapped[list["ComicGenre"]] = relationship(
        "ComicGenre",
        passive_deletes=True,
        foreign_keys="ComicGenre.genre_id"
    )



class ComicGenre(Base):
    __tablename__ = "comic_genres"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
        )
    comic_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE")
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE")
    )