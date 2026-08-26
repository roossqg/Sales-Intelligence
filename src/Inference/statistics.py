import pandas as pd
from scipy.stats import skewtest,shapiro,kurtosis,chisquare,poisson,expon,binom
import numpy as np

from datetime import datetime
from data_loading.importing import import_data
from data_loading.processing import process_data

import plotly.express as px

data_im = import_data('csv','sales.csv')
data_cl = process_data(data_im)

print(len(data_cl.columns))


def mean_ticket_month(data: pd.DataFrame):

    total_revenue = data.groupby('Month')['price'].agg('sum') / data.groupby('Month')['client_id'].agg('count')
    data = pd.DataFrame({'Month':total_revenue.index,'Revenue':list(total_revenue)})

    fig = px.line(data,x='Month',y='Revenue',title='Average Ticket Price per Month')

    return fig


def determine_the_normality_of_data(data: pd.DataFrame,col: str) -> dict:

    analyst = {
            'skew': skewtest(data[col]).statistic,
            'shapiro': shapiro(data[col]).pvalue,
            'kurtosis': kurtosis(data[col]),
            'test':0
            
        }

    if len(data) < 50:
            analyst['test'] = 'Non_Parametric'
            return analyst


    if analyst['skew'] <= 0.5 and analyst['shapiro'] <= 0.05 and analyst['kurtosis'] <= 0.3:
        analyst['test'] = 'Parametric'

    else:
        analyst['test'] = 'Non_Parametric'

    return analyst


def chi_square_tests(data: pd.DataFrame,col: str) -> float:

    observed = data[col].value_counts()
    proportions = data[col].value_counts(normalize=True)
    expected = proportions * len(data)

    chi_stat,pval = chisquare(f_exp=expected,f_obs=observed)

    return pval


def prob_quantity_per_time(data: pd.DataFrame,quantity: int,time: datetime) -> float:

    mean_solds_time =  data.groupby(time)['quantity'].agg('sum').mean()
    prob_qtd_time = poisson.cdf(range,mean_solds_time)

    return prob_qtd_time


def prob_revenue_per_time(data: pd.DataFrame,revenue: float,time: datetime) -> float:

    mean_revenue_time =  data.groupby(time)['price'].agg('sum').mean()
    prob_revenue_time = poisson.cdf(revenue,mean_revenue_time)

    return prob_revenue_time
   

def prob_sell_specific_product_sector(data: pd.DataFrame,n_product: int ,n_products: int,product: str) -> float:

    p_val_groups = chi_square_tests(data,'product_name')
    if p_val_groups >= 0.05:
        print('ChiSquare Goodness-of-Fit Test p-value >5%')
    else:
        print('ChiSquare Goodness-of-Fit Test p-value <5%!!')

    data_product = data[(data['product_name'] == product)]
    prob_product = len(data_product) / len(data)

    bin_dist = binom.cdf(n_product,prob_product,size=n_products)

    return bin_dist


#def age_cat_test_group

#def cat_quant_test

#def cat_price_test

#def expon_for