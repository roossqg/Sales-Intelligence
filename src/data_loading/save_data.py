import pandas as pd

from database import session,sales
from src.data_loading.processing import main
from src.data_loading.imports import load_data
from sqlalchemy.orm import Session


file_path = ''
data = pd.read_csv(file_path)

data_loaded = load_data(data)

data_processed = main(data_loaded)


def save_data_in_database(session: Session,data):

    for index,row in data.iterrows():

        data = row.to_dict()

        new_record = sales(data)

        session.add(new_record)

    session.commit()





