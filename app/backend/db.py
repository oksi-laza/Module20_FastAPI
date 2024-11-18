from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///cozy_house.db', echo=True)

SessionLocal = sessionmaker(bind=engine)    # создаем сессию связи с нашей БД


class Base(DeclarativeBase):
    """A base class for creating database table models.
    It is needed for mapping (combining) python model classes and database tables."""
    pass
