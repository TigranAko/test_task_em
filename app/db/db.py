from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError


url_db = "sqlite:///database.db"  # при необходимости модно поменять на постгрес
engine = create_engine(
    url_db,
    connect_args={"check_same_thread": False},  # для Sqlite
    poolclass=StaticPool,  # для sqlite
    echo=True,
)


@event.listens_for(engine, "connect")
def enable_sqlite_fk(dbapi_connection, _):
    """
    Для сохранения связей в sqlite
    При использовании постгреса удалить эту функцию
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # Включаем поддержку FK
    cursor.close()


LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class BaseModel(DeclarativeBase):
    pass


def create_tables():
    from models.access_roles_rules import AccessRolesRules
    from models.business_elements import BusinessElement
    from models.roles import Role
    from models.sessions import Session as SessionModel
    from models.users import User

    from repositories.users import UserRepository
    from repositories.roles import RoleRepository
    from repositories.business_elements import BusinessElementRepository
    from repositories.access_roles_rules import AccessRolesRulesRepository

    print(AccessRolesRules, BusinessElement, Role, SessionModel, User)
    BaseModel.metadata.create_all(engine)

    warnings = []
    with engine.connect() as db:
        role_repo = RoleRepository(db)
        roles = ["admin", "user", "guest", "manager"]
        for role in roles:
            try:
                role_repo.add_one({"name": role})
            except IntegrityError as e:
                warnings.append(("Роль", role, e))

        business_elements = ["users", "permissions", "products"]
        business_element_repo = BusinessElementRepository(db)
        for business_element in business_elements:
            try:
                business_element_repo.add_one({"name": business_element})
            except IntegrityError as e:
                warnings.append(("Бизнес элемент", role, e))

        try:
            user_repo = UserRepository(db)
            role_repo = RoleRepository(db)

            admin = {
                "firstname": "admin",
                "email": "admin@example.com",
                "password_hash": "admin",
                "role_id": role_repo.get_id("admin"),
            }
            user_repo.add_one(admin)
        except IntegrityError as e:
            warnings.append(("Админ", e))

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
                    warnings.append((role, element, e))

        db.commit()
    if warnings:
        if len(warnings) != 16:
            print("Предупреждения при заполнении таблиц:")
            for warning in warnings:
                print(" " * 4, warning, sep="")
        else:
            print("Предупреждений призаполнении БД:", len(warnings))
            print("4 роли, 3 бинесс элемента, 1 админ, 8 разрешений")
        print(
            "Эти предупреждения связаны с повторным запусом программы.\nОни не повлияют на работоспособность программы."
        )


def get_session():
    session: Session = LocalSession()
    try:
        yield session
    finally:
        session.close()
