from sqlalchemy.orm import Session
from db.db import BaseModel
from sqlalchemy import insert, select, update


class SQLAlchemyRepository:
    model: BaseModel

    def __init__(self, session: Session):
        self.session: Session = session

    def add_one(self, entity):
        stmt = insert(self.model).values(**entity).returning(self.model.id)
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        self.session.commit()
        return answer

    def find_all(self):
        stmt = select(self.model)  # TODO: Добавить фильтрацию и пагинацию
        result = self.session.execute(stmt)
        answer = result.scalars().all()
        return answer

    def find_one(self, entity_id):
        stmt = select(self.model).where(self.model.id == entity_id)
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    def edit_one(self, entity_id, entity):
        stmt = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**entity)
            .returning(self.model.id)
        )
        result = self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        self.session.commit()
        return answer
