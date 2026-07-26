from sqlalchemy import create_engine,Column,Integer,Float,String,DateTime
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass,Mapped,mapped_column,sessionmaker
from datetime import datetime

import os

DATABASE_URL = os.getenv('DATABASE_URL')

class Base(DeclarativeBase,MappedAsDataclass):
    pass


class sales(Base):

    __tablename__ = 'Sales_data'

    id : Mapped[int] = mapped_column(primary_key=True)
    client_id : Mapped[int]
    age : Mapped[int]
    price : Mapped[float]
    quantity : Mapped[int]
    age_range : Mapped[str]
    category : Mapped[str]
    datetime : Mapped[datetime]

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = session = Session()



