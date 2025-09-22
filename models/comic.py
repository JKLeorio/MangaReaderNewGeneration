import typing

from datetime import date
from sqlalchemy import Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.types import ComicTypes, ReleaseStatus, TranslateStatus
from .base import Base

if typing.TYPE_CHECKING:
    from models.association import Cover
    from models.person import Person
    from models.user import User
    from models.image import Image


class Comic(Base):
    __tablename__ = "comics"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    title: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    type: Mapped[ComicTypes] = mapped_column(
        Enum(ComicTypes),
        default=ComicTypes.MANGA
    )
    release_date: Mapped[int] = mapped_column(
        Integer
    )

    # release_status: Mapped[ReleaseStatus] = mapped_column(
    #     Enum(ReleaseStatus), default=ReleaseStatus.FROZEN
    # )
    # translate_status: Mapped[TranslateStatus] = mapped_column(
    #     Enum(TranslateStatus), default=TranslateStatus.NOT_TRANSLATED
    # )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="SET NULL"),
        nullable=True
        )
    author: Mapped["Person"] = relationship(
        "Person",
        back_populates="comics_author",
        passive_deletes=True
    )

    artist_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="SET NULL"),
        nullable=True
    )
    artist: Mapped["Person"] = relationship(
        "Person",
        back_populates="comics_artist",
        passive_deletes=True
    )
    covers: Mapped[list["Cover"]] = relationship(
        "Cover",
        back_populates="comic",
    )



class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    title: Mapped[str] = mapped_column(
        String
    )
    comic_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE")
    )
    comic: Mapped["Comic"] = relationship(
        "Comic",
        passive_deletes=True
    )
    position: Mapped[int] = mapped_column(
        Integer
    )
    volume: Mapped[int] = mapped_column(
        Integer
    )

    pages: Mapped[list["Page"]] = relationship(
        "Page",
        back_populates="chapter"
    )

    

class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    
    position: Mapped[int] = mapped_column(
        Integer
    )
    chapter_id: Mapped[int] = mapped_column(
        ForeignKey("chapters.id", ondelete="CASCADE")
    )
    chapter: Mapped["Chapter"] = relationship(
        "Chapter",
        back_populates="pages",
        passive_deletes=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True
    )
    image: Mapped["Image"] = relationship(
        "Image",
        passive_deletes=True
    )
