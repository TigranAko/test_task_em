from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.db import BaseModel
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .access_roles_rules import AccessRolesRules


class BusinessElement(BaseModel):
    __tablename__ = "business_element"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(), unique=True)
    access_roles_rules: Mapped[list["AccessRolesRules"]] = relationship(
        back_populates="element"
    )
