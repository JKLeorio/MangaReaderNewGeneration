from tkinter import Image
import typing

from sqlalchemy import ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from db.types import UserLIbraryItemStatus

if typing.TYPE_CHECKING:
    from models.comic import Comic
    from models.user import User

class UserLibraryItem(Base):
    __tablename__ = "user_library_items"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    type: Mapped[int] = mapped_column(
        Enum(UserLIbraryItemStatus), default=UserLIbraryItemStatus.READING
    )
    comic_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE")
        )
    comic: Mapped["Comic"] = relationship(
        "Comic",
        passive_deletes=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
        )
    user: Mapped["User"] = relationship(
        "User",
        passive_deletes=True
    )



class Cover(Base):
    __tablename__ = "covers"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    position: Mapped[int] = mapped_column(
        Integer
    )

    comic_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE"),
        # nullable=True
    )
    comic: Mapped["Comic"] = relationship(
        "Comic",
        back_populates="covers",
        passive_deletes=True
    )

    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="CASCADE"),
        # nullable=True
    )
    image: Mapped["Image"] = relationship(
        "Image",
        passive_deletes=True
    )