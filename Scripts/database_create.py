from database import session,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from settings import settings

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = session = Session()
