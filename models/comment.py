import typing

from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    page_id: Mapped[int] = mapped_column(
        ForeignKey("pages.id", ondelete="CASCADE")
    )
    page: Mapped["Page"] = relationship(
        "Page",
        passive_deletes=True
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
        passive_deletes=True
    )

    parent_id: Mapped[int] = mapped_column(
        ForeignKey("comments.id", ondelete="SET NULL")
    )
    
    childrens: Mapped[list["Comment"]] = relationship(
        "Comment"
    )