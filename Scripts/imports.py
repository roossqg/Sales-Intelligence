import pandas as pd
from functools import partial

from data_classes import DataLoadError

from sqlalchemy import create_engine

#select formats: []

input_format = input('define you file type: ')

#if input_format == 'sql':
#url = input()
#engine = create_engine(url)
    

formats = {'csv':pd.read_csv,
           'excel':pd.read_excel,
           'parquet':pd.read_parquet,
           'tsv':partial(pd.read_csv,sep='\t'),
           'json':pd.read_json,
           #'sql':partial(pd.read_sql,con=engine)
           }


def load_data(input_format:str,input_data:str,**kwargs) -> pd.DataFrame:

    if input_format not in formats.keys():
        raise DataLoadError(
            f"Format : '{input_format}' not supported",
            f"Formats supported : {list(formats.keys())}"
        )

    try:
        data = formats[input_format](input_data,**kwargs)

    except FileNotFoundError:
        raise DataLoadError(f"File: '{input_data}' not found")

    except pd.errors.EmptyDataError:
        raise DataLoadError(f"File: '{input_data}' is empty")

    except Exception as e:
        raise DataLoadError(f"Fail in read {input_data} as {input_format}: {e}") from e

    if data.empty:
        raise DataLoadError(f"Loaded Data: {input_data} are empty after load")

    return data

    
data = load_data('csv','synthetic_credit_dataset.csv')
##==================data formating===========================

#select cols to pattern: clients needs to be know

client_id = input('Change_by: ')
price = input('Change_by: ')
quantity = input('Change_by: ')
date = input('Change_by: ')
category = input('Change_by: ')


data.rename(
    columns={client_id :'client_id',
                    price:'price',
                    quantity:'quantity',
                    date:'date',
                    category:'category'},
                    inplace=True)


data = data[['client_id','price','quantity','date','category']]
print(data)
#save in local db


