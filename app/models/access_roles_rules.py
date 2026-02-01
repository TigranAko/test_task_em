from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.db import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .roles import Role
    from .business_elements import BusinessElement


class AccessRolesRules(BaseModel):
    __tablename__ = "access_roles_rules"
    __table_args__ = (
        UniqueConstraint("role_id", "element_id", name="uq_role_element"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="access_roles_rules")

    element_id: Mapped[int] = mapped_column(ForeignKey("business_element.id"))
    element: Mapped["BusinessElement"] = relationship(
        back_populates="access_roles_rules"
    )

    read_permission: Mapped[bool] = mapped_column(default=False)
    read_all_permission: Mapped[bool] = mapped_column(default=False)
    create_permission: Mapped[bool] = mapped_column(default=False)
    update_permission: Mapped[bool] = mapped_column(default=False)
    update_all_permission: Mapped[bool] = mapped_column(default=False)
    delete_permission: Mapped[bool] = mapped_column(default=False)
    delete_all_permission: Mapped[bool] = mapped_column(default=False)
