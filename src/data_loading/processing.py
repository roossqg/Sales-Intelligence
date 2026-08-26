import pandas as pd
import numpy as np

def datetime_numbers(data: pd.DataFrame,target_col: str = 'datetime') -> pd.DataFrame:
    '''create num columns from datetime to use in random forest'''

    data[target_col] =  pd.to_datetime(data[target_col])

    data['Year'] = data[target_col].dt.year
    data['Month'] = data[target_col].dt.month
    data['Day'] = data[target_col].dt.day
    data['Day_of_week'] = data[target_col].dt.dayofweek

    return data


def input_missing_values(data: pd.DataFrame) -> pd.DataFrame:

    inputs = {
        'age':data['age'].mean(),
        'price': data['price'].mean(),
        'quantity': data['quantity'].mean(),
        'product_name': "Unknown Product",
        'category': 'Unknown Category'
    }

    data.fillna(value=inputs,inplace=True) # -> input null features
    data = datetime_numbers(data)

    
    return data


def standardize_data(data: pd.DataFrame,col: str) -> pd.DataFrame:

    data[col] = data[col].str.strip()
    data[col] = data[col].str.replace(r's+',' ',regex=True)

    #irr chars
    data[col] = data[col].str.replace(r'[^a-zA-Z0-9À-ÿ\s]','',regex=True)

    return data[col]


def convert_data(data: pd.DataFrame) -> pd.DataFrame:

    for col in data.columns:
        if col in ['age','quantity','price','client_id']:
            data[col] = data[col].astype(int)
        else:
            pass

    data['datetime'] = pd.to_datetime(data['datetime'],errors='coerce',format='%Y-%m')
    
    data['category'] = data['category'].str.lower()
    data['category'] = standardize_data(data,'category')
    data['category'] = data['category'].astype('category')

    categories_age = pd.cut(data['age'],bins=[0,18,25,32,45,55,65,np.inf],
        labels=['-18','18-25','25-32','32-45','45-55','55-65','65+'])
    
    data['age_range'] = categories_age

    return data


def process_data(data: pd.DataFrame) -> pd.DataFrame:

    data_clean = input_missing_values(data)
    data_converted = convert_data(data_clean)

    return data_converted
