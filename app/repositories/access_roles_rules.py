from utils.base_repository import SQLAlchemyRepository
from models.access_roles_rules import AccessRolesRules
from sqlalchemy import select, and_


class AccessRolesRulesRepository(SQLAlchemyRepository):
    model = AccessRolesRules

    def get_rule(self, entity_id, role_id):
        stmt = select(self.model).where(
            and_(self.model.element_id == entity_id, self.model.role_id == role_id)
        )
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
