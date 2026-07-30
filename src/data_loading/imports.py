import pandas as pd
from functools import partial


#import Models.data_classes

from sqlalchemy import create_engine
import sqlite3

#i = Models.data_classes.DataLoadError

#input_format = input('define you file type: ')

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
        raise FileExistsError(
            f"Format : '{input_format}' not supported",
            f"Formats supported : {list(formats.keys())}"
        )

    try:
        data = formats[input_format](input_data,**kwargs)

    except FileNotFoundError:
        raise FileExistsError(f"File: '{input_data}' not found")

    except pd.errors.EmptyDataError:
        raise FileExistsError(f"File: '{input_data}' is empty")

    except Exception as e:
        raise FileExistsError(f"Fail in read {input_data} as {input_format}: {e}") from e

    if data.empty:
        raise FileExistsError(f"Loaded Data: {input_data} are empty after load")

    return data


def rename_columns(data,client_id:str,
                   price:str,quantity:str,datetime:str,category:str,age:str,product_name:str):

    data.rename(
        columns={client_id :'client_id',
                 #product_name: 'product_name',
                        price:'price',
                        quantity:'quantity',
                        datetime:'datetime',
                        category:'category',
                        age:'age'},
                        inplace=True)

    data = data[['client_id','price','quantity','category','age','datetime','product_name']]

    return data


def import_data(file_type,file_path):

    data = load_data(file_type,file_path)
    data = rename_columns(data,'client_id','price','quantity','datetime','category','age','product_name')
    data = data[['client_id','price','quantity','datetime','category','age','product_name']]

    return data


#test:
data = pd.DataFrame({
    'client_id':[1,2,3,4,5],
    'price': [22.3,555,23,67,1000],
    'quantity':[2,4,7,20,1000],
    'datetime':['2013-02-10','2013-02-11','2013-02-10','2013-02-16','2013-04-10'],
    'category':['sports','','sports','','games'],
    'age':[22,34,19,87,27],
    'product_name': ['ball','plane','boil','ball','book']
})
data = data[['client_id','price','quantity','datetime','category','age','product_name']]
data.to_csv('sales.csv',index=False)
