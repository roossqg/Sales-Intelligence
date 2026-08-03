from src.data_loading.importing import import_data
from src.data_loading.processing import process_data

from sqlalchemy.orm import Session
from src.database.database_create import get_session
from src.database.database_processing import export_to_sql
from src.Models.database import engine

def get_data(file_type,file_path):

    data_import = import_data(file_type,file_path)
    data_process = process_data(data_import)
    print(data_process)

    message = export_to_sql(engine,data_process,'Sales_data',get_session)

    return message

print(get_data('csv','sales.csv'))