from data_loading.importing import import_data
from data_loading.processing import process_data

from database.database_create import get_session
from database.database_processing import export_to_sql

def get_data(file_type,file_path):

    data_import = import_data(file_type,file_path)
    data_process = process_data(data_import)

    message = export_to_sql(get_session,data_process)

    return message
