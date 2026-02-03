from sqlalchemy.orm import Session
from repositories.users import UserRepository
from repositories.business_elements import BusinessElementRepository
from repositories.access_roles_rules import AccessRolesRulesRepository

from fastapi import Depends
from db.db import get_session

from fastapi import HTTPException, status


class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def has_permission(self, user_id: int, element: str, action: str) -> bool:
        """Проверяет разрешение без детальной логики владельца"""
        # Получаем пользователя
        user_repo = UserRepository(self.db)
        user = user_repo.find_one(user_id)
        print(user)
        print(user.role_id)
        print(user.role.name)
        if not user or not user.role_id:
            return False

        # Получаем элемент
        element_repo = BusinessElementRepository(self.db)
        biz_element_id = element_repo.get_id(element)
        print(biz_element_id)
        if not biz_element_id:
            return False

        # Получаем правило
        rule_repo = AccessRolesRulesRepository(self.db)
        rule = rule_repo.get_rule(user.role_id, biz_element_id)
        print(rule, rule.read_all_permission)
        print(rule.role.name)
        if not rule:
            return False

        # Простая проверка по действию
        if action == "read":
            return rule.read_permission
        elif action == "read_all":
            return rule.read_all_permission
            ...
        elif action == "create":
            return rule.create_permission
        elif action == "update":
            return rule.update_permission or rule.update_all_permission
        elif action == "delete":
            return rule.delete_permission or rule.delete_all_permission

        return False


def get_permission_service(session: Session = Depends(get_session)):
    return PermissionService(session)


def check_permission(element: str, action: str):
    """Простая зависимость для проверки прав"""
    from api.users import get_current_user

    def dependency(
        current_user: dict = Depends(get_current_user), db=Depends(get_session)
    ):
        service = PermissionService(db)
        if not service.has_permission(current_user.id, element, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No permission to {action} {element}",
            )
        return current_user

    return dependency
