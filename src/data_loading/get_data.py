import pandas as pd
from imports import import_data
from processing import process


data_processed = import_data('csv','sales.csv')
data_processed = process(data_processed)
print(data_processed)
