import pytest
import pandas as pd

from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app.app import load_data

@pytest.fixture
def create_clean_data():

    data = pd.DataFrame({
    'client_id':[1,2,3,4,5],
    'price': [22.3,555,23,67,1000],
    'quantity':[2,4,7,20,1000],
    'datetime':['2013-02-10','2013-02-11','2013-02-10','2013-02-16','2013-04-10'],
    'category':['sports','tech','sports','food','games'],
    'age':[22,34,19,87,27],
    'product_name': ['ball','plane','boil','ball','book']
    })

    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data[['client_id','price','quantity','datetime','category','age','product_name']]
    return data

@pytest.fixture
def data_format_path():
    return ['csv','sales4.csv']


@pytest.fixture
def data_full(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data = load_data(data_pr)

    return data

