from utils.base_repository import SQLAlchemyRepository
from models.roles import Role


class RoleRepository(SQLAlchemyRepository):
    model = Role
