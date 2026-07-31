from src.data_loading.importing import import_data
import pandas as pd

def test_import(data_format_path):

    data_processed = import_data(data_format_path[0],data_format_path[1])

    assert type(data_processed) == pd.DataFrame