import pandas as pd
import numpy as np

data = pd.read_csv('sales.csv')


#conceptual input
def input_missing_vals_data(data):

######################conceptual:

    inputs = {
        'client_id': data['client_id'].unique()[-1] + 1,
        'age':data['age'].mean(),
        'date':data['date'].mean(),

        'age_range':pd.cut(data['age']),

        'quantity':data.groupby('category')['quantity'].mean(),
        'category:rd(data),'
        'price':data.groupby('category')['price'].mean(),
    }


    data.fillna(values=inputs,inplace=True)
    return data


def convert_data(data):

    for col in data.columns:

        if col in ['age','quantity','price','client_id']:
            data[col] = data[col].astype(int)

        if col == 'date':
            data[col] = pd.to_datetime(data[col],format='%Y-%m-%d : %H')

        if col == 'age_range': 
            categories_age = pd.cut(data['age'],bins=[0,18,25,32,45,55,65,np.inf],
                labels=['-18','18-25','25-32','32-45','45-55','55-65','65+'])
            data[col] = categories_age

        if col == 'category':
            data[col] = data[col].astype('category')

    return data


def standardize_data(data,col):

    #1.clean all irregular chars
    #2.clear all blank spaces for ' '
    #3.remove incosistent cats

    #blank sp
    data[col] = data[col].str.strip()
    data[col] = data[col].str.replace(r's+',' ',regex=True)
    #irr chars
    data[col] = data[col].str.replace(r'[^a-zA-Z0-9À-ÿ\s]','',regex=True)

    return data[col]

        
    



## create/pattern:
#models: 
#cust_id : int-duplicate, : last_id + 1

#age:int (5-80)->age_cat: [6 cats]:cat :  mean if null

#quant: int -no limit : mean per cat ifnull

#cat: cat-> sectors/type -> random forest-input if null

#price $ : int: mean per cat if null

#date: datetime (y-m-d : hr) : mean if null






##sqlite
