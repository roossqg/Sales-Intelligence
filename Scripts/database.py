from sqlalchemy import create_engine,Column,Integer,Float,String,DateTime,func
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass,Mapped,mapped_column,sessionmaker
from datetime import datetime
from typing import Optional

import os

from settings import settings

class Base(DeclarativeBase,MappedAsDataclass):
    pass


class sales(Base):

    __tablename__ = 'Sales_data'

    id : Mapped[int] = mapped_column(primary_key=True)
    client_id : Mapped[Optional[int]] = mapped_column(nullable=True) 
    age : Mapped[Optional[int]] = mapped_column(nullable=True) 
    price : Mapped[Optional[float]] = mapped_column(nullable=True) 
    quantity : Mapped[Optional[int]] = mapped_column(nullable=True) 
    age_range : Mapped[Optional[str]] = mapped_column(nullable=True) 
    category : Mapped[Optional[str]] = mapped_column(nullable=True) 
    datetime : Mapped[datetime] #= mapped_column(DateTime,server_default=func.now())

engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = session = Session()

print('sss')

#add data
#session.add(sales(age=45,id=2,client_id=4,price=3.4,quantity=33,age_range='44',category='sports'))
print('adding')

session.commit()
print('commit !!')

print(session.query(sales).all())



