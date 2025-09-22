import typing
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    String, 
    DateTime, 
    Integer, 
    Enum
    )
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import (
    datetime,
    date
    )

from db.types import Role
from .base import Base

if typing.TYPE_CHECKING:
    from .image import Image


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
        )
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role", create_type=True), default=Role.USER)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    avatar_id: Mapped[int] = mapped_column(
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True
        )
    avatar: Mapped["Image"] = relationship(
        "Image",
        passive_deletes=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
