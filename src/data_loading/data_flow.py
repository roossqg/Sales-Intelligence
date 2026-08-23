from data_loading.importing import import_data
from data_loading.processing import process_data
import pandas as pd
from database.database_processing import export_to_sql
from database.database_create import engine

def export_data_sql(file_type,file_path):

    data_import = import_data(file_type,file_path)
    data_process = process_data(data_import)
    print(data_process)

    message = export_to_sql(engine,data_process)

    return message


def get_data_sql(engine=engine):

    df = pd.read_sql('SELECT * FROM Sales_data;',engine)
    return df