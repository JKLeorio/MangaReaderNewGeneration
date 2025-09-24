import typing
from .base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

if typing.TYPE_CHECKING:
    from .user import User

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
    url: Mapped[str] = mapped_column(String)
    filename: Mapped[str] = mapped_column(String)
    extension: Mapped[str] = mapped_column(String)
    uploaded_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    uploaded_by: Mapped["User"] = relationship(
        "User",
        foreign_keys=[uploaded_by_id],
        passive_deletes=True,
    )

    # covers: Mapped["Cover"]
    # pages: Mapped["Page"]
