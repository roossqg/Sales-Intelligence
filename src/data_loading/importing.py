import pandas as pd

from functools import partial



formats = {'csv':pd.read_csv,
           'excel':pd.read_excel,
           'parquet':pd.read_parquet,
           'tsv':partial(pd.read_csv,sep='\t'),
           'json':pd.read_json,
           }


def load_data(input_format: str,input_data: str,**kwargs) -> pd.DataFrame:

    if input_format not in formats.keys():
        raise FileExistsError(
            f"Format : '{input_format}' not supported",
            f"Formats supported : {list(formats.keys())}"
        )

    try:
        data = formats[input_format](input_data,**kwargs)

    except FileExistsError:
        raise FileExistsError(f"File: '{input_data}' not found")

    except pd.errors.EmptyDataError:
        raise FileExistsError(f"File: '{input_data}' is empty")

    except Exception as e:
        raise FileExistsError(f"Fail in read {input_data} as {input_format}: {e}") from e

    if data.empty:
        raise FileExistsError(f"Loaded Data: {input_data} are empty after load")

    return data


def rename_columns(data: pd.DataFrame,client_id: str,
                   price: str,quantity: str,datetime: str,
                   category: str,age: str,product_name: str) -> pd.DataFrame:

    data.rename(
        columns={client_id :'client_id',
                 product_name: 'product_name',
                        price:'price',
                        quantity:'quantity',
                        datetime:'datetime',
                        category:'category',
                        age:'age'},
                        inplace=True)

    data = data[['client_id','price','quantity','category','age','datetime','product_name']]

    return data


def import_data(file_type: str,file_path: str) -> pd.DataFrame:

    data_loaded = load_data(file_type,file_path)
    data_columns_renamed = rename_columns(data_loaded,'client_id','price','quantity','datetime','category','age','product_name')
    data_imported = data_columns_renamed[['client_id','price','quantity','datetime','category','age','product_name']]

    return data_imported


