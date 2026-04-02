# Этот код не используется
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import BaseModel
from sqlalchemy import String, ForeignKey
from datetime import datetime, timedelta, UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


class Session(BaseModel):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")

    token: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    expires_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC) + timedelta(days=7)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
"""
