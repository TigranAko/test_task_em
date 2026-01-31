from utils.base_repository import SQLAlchemyRepository
from models.access_roles_rules import AccessRolesRules


class AccessRolesRulesRepository(SQLAlchemyRepository):
    model = AccessRolesRules
