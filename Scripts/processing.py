import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('sales.csv')


def datetime_numbers(data,target_col = 'datetime'):

    data[target_col] = data[target_col].astype('datetime')

    data['Year'] = data['datetime'].dt.year
    data['Month'] = data['datetime'].dt.month
    data['Day'] = data['datetime'].dt.day
    data['Day_of_week'] = data['datetime'].dt.dayofweek

    data = data.drop(columns=[target_col])

    return data


def input_category(data,target_col = 'category'):

    predict_y_set = data[data[target_col].isna()] # data for input

    features = [col for col in data.columns if col != target_col]

    train_x_set = data[data[features].notna()] # clean features
    train_y_set = data[data[target_col].notna()] # clean target

    train_x_set = datetime_numbers(train_x_set) # get numbers dataframe

    inputer = RandomForestClassifier(n_estimators=200,max_samples=300,criterion='log_loss')
    inputer.fit(train_x_set,train_y_set)

    #fill
    data.loc[data[target_col].isna(),target_col] = inputer.predict(predict_y_set)
        
   ## limit train set size for small training times,log loss for num features
    return data


#conceptual input
def input_missing_vals_data(data):

    inputs = {
        'age':data['age'].mean(),
        #date,id -> type: int/datetime,null values- show in stats : Unknow_date,Unknow_id
    }

    #random forest in no null values
    data = input_category(data)

    data.fillna(values=inputs,inplace=True) # -> input null features

    #after input cats
    data[['price','quantity']] = data.groupby('category')[['price','quantity']].transform(
                lambda x: x.fillna(x.mean))
    
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


def convert_data(data):

    for col in data.columns:


        if col in ['age','quantity','price','client_id']:
            data[col] = standardize_data(data,col)
            data[col] = data[col].astype(int)

        if col == 'datetime':
            data[col] = pd.to_datetime(data[col],format='%Y-%m-%d : %H')


        elif col == 'category':
            data[col] = data[col].str.lower()
            data[col] = standardize_data(data,col)
            data[col] = data[col].astype('category')

        else:
            pass

        
    categories_age = pd.cut(data['age'],bins=[0,18,25,32,45,55,65,np.inf],
        labels=['-18','18-25','25-32','32-45','45-55','55-65','65+'])
    
    data['age_range'] = categories_age

    return data


input_missing_vals_data(convert_data(data)).to_csv('clean_sales.csv')
    
#order :
#standarlize(convert()) -> datetime -> inp_cat(datetime) -> miss(inp_cat))
# =  convert(std(data)) -> miss(inp_cat(datetime(data))-> inputs) -> clean data


#cust_id : null

#age:int (5-80)->age_cat: [6 cats]:cat :  mean if null

#quant: int -no limit : mean per cat ifnull

#cat: cat-> sectors/type -> random forest-input if null

#price $ : int: mean per cat if null

#date: datetime (y-m-d : hr) : mean if null

#future:
#transaction_id : data inputs





##sqlite
