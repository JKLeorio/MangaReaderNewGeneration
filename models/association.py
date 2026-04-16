import typing

from sqlalchemy import Column, ForeignKey, Enum, Integer, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column


from .base import Base
from db.types import UserLIbraryItemStatus

if typing.TYPE_CHECKING:
    from models.image import Image
    from models.comic import Comic
    from models.user import User

class UserLibraryItem(Base):
    __tablename__ = "user_library_items"

    # id: Mapped[int] = mapped_column(
    #     Integer, 
    #     primary_key=True, 
    #     autoincrement=True
    #     )
    type: Mapped[UserLIbraryItemStatus] = mapped_column(
        Enum(UserLIbraryItemStatus), default=UserLIbraryItemStatus.READING
    )
    comic_id: Mapped[int] = mapped_column(
        ForeignKey("comics.id", ondelete="CASCADE"),
        primary_key=True
        )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
        )
    comic: Mapped["Comic"] = relationship()


comic_genre_association_table= Table(
    "comic_genres",
    Base.metadata,
    Column(
        "comic_id", ForeignKey(
            "comics.id",
            ondelete="CASCADE",
        ),
        primary_key=True
    ),
    Column(
        "genre_id", ForeignKey(
            "genres.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)



# class Cover(Base):
#     __tablename__ = "covers"

#     id: Mapped[int] = mapped_column(
#         Integer, 
#         primary_key=True, 
#         autoincrement=True
#         )
#     position: Mapped[int] = mapped_column(
#         Integer
#     )

#     comic_id: Mapped[int] = mapped_column(
#         ForeignKey("comics.id", ondelete="CASCADE"),
#         # nullable=True
#     )
#     comic: Mapped["Comic"] = relationship(
#         "Comic",
#         foreign_keys=[comic_id],
#         back_populates="covers",
#         passive_deletes=True
#     )

#     image_id: Mapped[int] = mapped_column(
#         ForeignKey("images.id", ondelete="CASCADE"),
#         # nullable=True
#     )
#     image: Mapped["Image"] = relationship(
#         "Image",
#         passive_deletes=True
#     )

#     @property
#     def image_url(self):
#         if self.image:
#             return self.image.url
#         return None