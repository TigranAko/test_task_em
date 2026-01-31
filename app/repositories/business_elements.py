from utils.base_repository import SQLAlchemyRepository
from models.business_elements import BusinessElement


class BusinessElementRepository(SQLAlchemyRepository):
    model = BusinessElement
