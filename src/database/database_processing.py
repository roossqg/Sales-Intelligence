from src.database.database_create import engine
import pandas as pd
from database.database_create import session
from sqlalchemy.orm import Session
from Models.database import sales


def export_to_sql(query='SELECT * FROM  sales'):

    df = pd.read_sql(query,engine)
    

def save_data_in_database(session: Session,data):

    for index,row in data.iterrows():

        data = row.to_dict()

        new_record = sales(data)

        session.add(new_record)

    session.commit()