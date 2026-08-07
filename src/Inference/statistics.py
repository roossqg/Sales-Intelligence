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
    fig.show()


#considerations
#normality of data: group num distributions and tests significance
#proprotions tests: group proportions signifcance

def boostrap_test(data: pd.DataFrame,col: str):
    #simple sampling

    size = len(data)
    boot_means = []

    for i in range(5000):
        boot_means.append(
            np.mean(data.sample(frac=0.3,replace=True)[col])
        )

    mean_sample = np.mean(boot_means)
    std_sample = np.std(boot_means,ddof=1)

    cohen_d = (mean_sample - np.mean(data[col])) / std_sample

    return cohen_d


def determine_the_normality_of_data(data: pd.DataFrame,col: str) -> dict:

    appropriate_tests = {'test': ''}

    if len(data) < 50:
            appropriate_tests['test'] = 'Non_Parametric' # small data size
            return appropriate_tests

    analyst = {
        'skew': skewtest(data[col]).statistic,
        'shapiro': shapiro(data[col]).pvalue,
        'kurtosis': kurtosis(data[col]).pvalue,
    }

    if analyst['skew'] <= 0.5 and analyst['shapiro'] <= 0.05 and analyst['kurtosis'] <= 0.3:
        appropriate_tests['test'] = 'Parametric'

    else:
        appropriate_tests['test'] = 'Non_Parametric'

    return appropriate_tests


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

    return data


#def age_cat_test_group

#def cat_quant_test

#def cat_price_test

#def expon_for