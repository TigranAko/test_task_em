from utils.base_repository import SQLAlchemyRepository
from models.users import User


class UserRepository(SQLAlchemyRepository):
    model = User
