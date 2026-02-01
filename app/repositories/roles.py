from utils.base_repository import SQLAlchemyRepository
from models.roles import Role
from sqlalchemy import select


class RoleRepository(SQLAlchemyRepository):
    model = Role

    def get_id(self, name: str) -> int:
        stmt = select(self.model.id).where(self.model.name == name)
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
