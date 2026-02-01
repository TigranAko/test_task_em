from db.db import get_session
from sqlalchemy.orm import Session
from repositories.roles import RoleRepository
from fastapi import Depends


class RoleService:
    def __init__(self, session: Session):  # , repository: UserRepository):
        self.db: Session = session
        # self.repo = repository
        self.repo = RoleRepository(session)


def get_user_service(session: Session = Depends(get_session)):
    return RoleService(session)
