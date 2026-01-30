from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from sqlalchemy.pool import StaticPool

url_db = "sqlite:///database.db"  # при необходимости модно поменять на постгрес
engine = create_engine(
    url_db,
    connect_args={"check_same_thread": False},  # для Sqlite
    poolclass=StaticPool,  # для sqlite
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


def get_session():
    session: Session = LocalSession()
    try:
        yield session
    finally:
        session.close()
