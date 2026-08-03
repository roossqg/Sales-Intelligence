from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.settings import settings
from contextlib import contextmanager

engine = create_engine(settings.DATABASE_URL)

@contextmanager
def get_session():
    with Session(engine,expire_on_commit=False) as session:
        yield session