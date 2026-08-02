from Models.database import session,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,Session
from settings import settings

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)


def get_session():
    with Session(engine,expire_on_commit=False) as session:
        yield session