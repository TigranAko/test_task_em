from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.db import BaseModel
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .roles import Role
    from .sessions import Session


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String())
    lastname: Mapped[str | None] = mapped_column(String(), default=None)
    patronymic: Mapped[str | None] = mapped_column(String(), default=None)
    email: Mapped[str] = mapped_column(String(), unique=True)
    password_hash: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    sessions: Mapped[list["Session"]] = relationship(back_populates="user")
