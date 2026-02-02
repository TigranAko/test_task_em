from utils.base_repository import SQLAlchemyRepository
from models.users import User
from sqlalchemy import select


class UserRepository(SQLAlchemyRepository):
    model = User

    def get_by_email(self, email):
        stmt = select(self.model).where(self.model.email == email)
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer
