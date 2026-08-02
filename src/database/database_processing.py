from database.database_create import engine
import pandas as pd
from database.database_create import session
from sqlalchemy.orm import Session
from Models.database import sales


def import_from_sql(query: str ='SELECT * FROM  sales') -> pd.DataFrame:

    df = pd.read_sql(query,engine)
    

def export_to_sql(session: Session,data: pd.DataFrame) -> str:

    for index,row in data.iterrows():

        data = row.to_dict()

        new_record = sales(data)

        session.add(new_record)

    session.commit()

    return "Data saved successfully!"