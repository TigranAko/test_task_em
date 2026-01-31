from utils.base_repository import SQLAlchemyRepository
from models.sessions import Session


class SessionRepository(SQLAlchemyRepository):
    model = Session
