from src.database.database_create import engine,get_session
import pandas as pd

from sqlalchemy.orm import Session
from src.Models.database import sales


def import_from_sql(query: str ='SELECT * FROM  sales') -> pd.DataFrame:

    df = pd.read_sql(query,engine)
    

def export_to_sql(engine,data: pd.DataFrame) -> str:

    with get_session(engine=engine)  as session:
        for index, row in data.iterrows():
            record_dict = row.to_dict()
            new_record = sales(**record_dict)
            session.add(new_record)

    session.commit()

    return "Data saved successfully!"