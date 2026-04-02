from repositories.users import UserRepository
from repositories.roles import RoleRepository
from repositories.business_elements import BusinessElementRepository
from repositories.access_roles_rules import AccessRolesRulesRepository
from services.users import get_user_service
from sqlalchemy.exc import IntegrityError
from db.db import engine


def create_roles():
    print("Создаются роли")
    roles = ["admin", "user", "guest", "manager"]
    with engine.connect() as db:
        role_repo = RoleRepository(db)
        for role in roles:
            try:
                role_repo.add_one({"name": role})
            except IntegrityError as e:
                print(("Роль", role, e))
        db.commit()


def create_bussiness_elements():
    print("Создютя бизнес элементы")
    business_elements = ["users", "permissions", "products"]
    with engine.connect() as db:
        business_element_repo = BusinessElementRepository(db)
        for business_element in business_elements:
            try:
                business_element_repo.add_one({"name": business_element})
            except IntegrityError as e:
                print(("Бизнес элемент", business_element, e))
        db.commit()


def create_admin():
    print("Создается админ")
    with engine.connect() as db:
        try:
            user_repo = UserRepository(db)
            role_repo = RoleRepository(db)
            user_service = get_user_service()

            admin = {
                "firstname": "admin",
                "email": "admin@example.com",
                "password_hash": user_service._hash_password("admin"),
                "role_id": role_repo.get_id("admin"),
                "is_active": True,
            }
            user_repo.add_one(admin)
        except IntegrityError as e:
            print(("Админ", e))
        db.commit()


def create_access():
    print("Создются разрешения")
    with engine.connect() as db:
        access_roles_rules_data = {
            "admin": {
                "users": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                },
                "products": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                },
                "permissions": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": True,
                    "delete_all_permission": True,
                },
            },
            "manager": {
                "users": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": False,
                    "update_permission": True,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },
                "products": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": True,
                    "update_permission": True,
                    "update_all_permission": True,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },
            },
            "user": {
                "users": {
                    "read_permission": True,
                    "read_all_permission": False,
                    "create_permission": False,
                    "update_permission": True,
                    "update_all_permission": False,
                    "delete_permission": True,
                    "delete_all_permission": False,
                },
                "products": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": False,
                    "update_permission": False,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },
            },
            "guest": {
                "products": {
                    "read_permission": True,
                    "read_all_permission": True,
                    "create_permission": False,
                    "update_permission": False,
                    "update_all_permission": False,
                    "delete_permission": False,
                    "delete_all_permission": False,
                },
            },
        }
        # можно использовать 1 репозиторий т.к. таблицы связаны
        role_repo = RoleRepository(db)
        business_element_repo = BusinessElementRepository(db)
        access_roles_rules_repo = AccessRolesRulesRepository(db)

        for role, datas in access_roles_rules_data.items():
            for element, data in datas.items():
                role_id = role_repo.get_id(role)
                business_element_id = business_element_repo.get_id(element)
                data |= {"role_id": role_id, "element_id": business_element_id}
                try:
                    access_roles_rules_repo.add_one(data)
                except IntegrityError as e:
                    print((role, element, e))

        db.commit()


def create_all():
    print("create all seeds")
    create_roles()
    create_bussiness_elements()
    create_admin()
    create_access()


if __name__ == "__main__":
    create_all()
