import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('sales.csv')


def datetime_numbers(data,target_col = 'datetime'):
    '''create num columns from datetime to use in random forest'''

    data[target_col] =  pd.to_datetime(data[target_col])

    data['Year'] = data[target_col].dt.year
    data['Month'] = data[target_col].dt.month
    data['Day'] = data[target_col].dt.day
    data['Day_of_week'] = data[target_col].dt.dayofweek

    return data


## limit train set size for small training times,log loss for num features
def input_missing_category(data,target_col = 'category'):

    data = datetime_numbers(data)

    df = data.drop(columns=['datetime']) # we already have date numbers

    features = [col for col in df.columns if col != target_col]
    
    non_null_df = df[df[target_col].notna()]
    null_df = df[df[target_col].isna()]
    
    if null_df.empty:
        return df
    
    X_train = non_null_df[features]
    y_train = non_null_df[target_col]

    X_pred = null_df[features]
    
    inputer = RandomForestClassifier(n_estimators=200,max_samples=300,criterion='log_loss')
    inputer.fit(X_train,y_train)

    data.loc[data[target_col].isna(),target_col] = inputer.predict(X_pred)

    return data


def input_missing_values(data):

    inputs = {
        'age':data['age'].mean(),
    }

    data.fillna(value=inputs,inplace=True) # -> input null features
    data = input_missing_category(data)

    #after input cats
    data[['price','quantity']] = data.groupby('category')[['price','quantity']].transform(
                lambda x: x.fillna(x.mean))
    
    return data


def standardize_data(data,col):

    data[col] = data[col].str.strip()
    data[col] = data[col].str.replace(r's+',' ',regex=True)

    #irr chars
    data[col] = data[col].str.replace(r'[^a-zA-Z0-9À-ÿ\s]','',regex=True)

    return data[col]


def convert_data(data):

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
    data = data.drop(columns=['Unnamed: 0']).reset_index(drop=True)

    return data


def main(data):

    data_clean = input_missing_values(data)
    data_converted = convert_data(data_clean)

    return data_converted

#future:
#transaction_id : data inputs

#print(main(data))
#corrections: std~convert funcs,