from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.db import BaseModel
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .access_roles_rules import AccessRolesRules


class Role(BaseModel):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(), unique=True
    )  # (админ, менеджер, пользователь, гость);

    users: Mapped[list["User"]] = relationship(back_populates="role")
    access_roles_rules: Mapped[list["AccessRolesRules"]] = relationship(
        back_populates="role"
    )
