import typing

from datetime import date
from sqlalchemy import Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.types import ComicType, ReleaseStatus, TranslateStatus
from .base import Base

from models.association import Cover

if typing.TYPE_CHECKING:
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
    type: Mapped[ComicType] = mapped_column(
        Enum(ComicType, name="comictypes"),
        default=ComicType.MANGA
    )
    release_date: Mapped[int] = mapped_column(
        Integer
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="SET NULL"),
        nullable=True
        )
    author: Mapped["Person"] = relationship(
        "Person",
        foreign_keys=[author_id],
        back_populates="comics_author",
        passive_deletes=True
    )
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="SET NULL"),
        nullable=True
    )
    artist: Mapped["Person"] = relationship(
        "Person",
        foreign_keys=[artist_id],
        back_populates="comics_artist",
        passive_deletes=True
    )
    covers: Mapped[list["Cover"]] = relationship(
        "Cover",
        back_populates="comic",
    )

    # release_status: Mapped[ReleaseStatus] = mapped_column(
    #     Enum(ReleaseStatus), default=ReleaseStatus.FROZEN
    # )
    # translate_status: Mapped[TranslateStatus] = mapped_column(
    #     Enum(TranslateStatus), default=TranslateStatus.NOT_TRANSLATED
    # )


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
        foreign_keys=[comic_id],
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
        foreign_keys=[chapter_id],
        back_populates="pages",
        passive_deletes=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True
    )
    image: Mapped["Image"] = relationship(
        "Image",
        foreign_keys=[image_id],
        passive_deletes=True
    )
    
    @property
    def image_url(self) -> str:
        return self.image.url

