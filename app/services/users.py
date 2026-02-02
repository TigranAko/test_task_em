from db.db import get_session
from sqlalchemy.orm import Session
from repositories.users import UserRepository
from schemas.users import UserCreate
from fastapi import Depends, HTTPException
from services.roles import RoleService
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService:
    def __init__(self, session: Session):  # , repository: UserRepository):
        self.db: Session = session
        # self.repo = repository
        self.repo = UserRepository(session)

    def register(self, user: UserCreate):
        role_service = RoleService(self.db)
        # role_id = role_service.get_or_create_role("user")
        role_id = role_service.repo.get_id("user")

        password = user.password
        if password != user.password_replay:
            raise HTTPException(400)
        data = user.model_dump()
        data.pop("password")
        data.pop("password_replay")
        print(data)
        password_hash = self._create_password_hash(password)
        data["password_hash"] = password_hash
        data["role_id"] = role_id
        data["is_active"] = True

        result = self.repo.add_one(data)
        return result

    def about(self): ...

    def login(self): ...

    def logout(self): ...

    def update(self): ...

    def _create_password_hash(self, password: str) -> str:
        password = password.encode("utf-8")
        return pwd_context.hash(password)


def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)
