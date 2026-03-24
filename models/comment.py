import typing

from datetime import datetime
from sqlalchemy import SmallInteger, Integer, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from db.types import CommentRefers
from utils.datetime_utils import get_current_time

from .base import Base

if typing.TYPE_CHECKING:
    from .user import User
    from .comic import Page


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
    content: Mapped[int] = mapped_column(
        Text
        )
    
    record_id: Mapped[int] = mapped_column(
        Integer
    )
    refers_to: Mapped[CommentRefers] = mapped_column(
        Enum(CommentRefers, names="comment_refers",),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id],
        passive_deletes=True
    )

    depth: Mapped[SmallInteger] = mapped_column(
        Integer,
        default=0
    )

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id", ondelete="SET NULL"),
        nullable=True
    )

    parent: Mapped["Comment"] = relationship(
        "Comment", back_populates="childrens", remote_side=[id]
    )
    
    childrens: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates='parent'
    )
    @validates("depth")
    def depth_max(self, key, depth: int):
        if not (5 >= depth >= 0):
            raise ValueError(
                "depth must be in range 0-5"
            )
        return depth