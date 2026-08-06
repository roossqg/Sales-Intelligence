from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.database.database_processing import export_to_sql
from sqlalchemy import create_engine
from src.Models.database import Base

import pandas as pd

def test_import_data(data_format_path: list):

    data_processed = import_data(data_format_path[0],data_format_path[1])

    assert type(data_processed) == pd.DataFrame
    assert list(data_processed.columns) == ['client_id','price','quantity','datetime','category','age','product_name']


def test_process_data(create_clean_data: pd.DataFrame,data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_processed = process_data(data_imp)

    assert type(data_processed) == pd.DataFrame
    assert len(data_processed.columns) == 12


def test_export_to_sql(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_processed = process_data(data_imp)

    engine = create_engine('sqlite:///:memory:')
    
    Base.metadata.create_all(engine)
    
    message = export_to_sql(engine,data_processed)
    
    Base.metadata.drop_all(engine)

    assert message == "Data saved successfully!"
