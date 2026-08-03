from src.database.database_create import engine
import pandas as pd

from sqlalchemy.orm import Session
from src.Models.database import engine,sales


def import_from_sql(query: str ='SELECT * FROM  sales') -> pd.DataFrame:

    df = pd.read_sql(query,engine)
    

def export_to_sql(engine,data: pd.DataFrame,table_name: str,session) -> str:

    session = Session(engine)
    for index, row in data.iterrows():
        record_dict = row.to_dict()
        new_record = sales(**record_dict)
        session.add(new_record)

    session.commit()

    return "Data saved successfully!"