import pandas as pd
from scipy.stats import skewtest,shapiro,kurtosis,poisson
import numpy as np

from data_loading.importing import import_data
from data_loading.processing import process_data

import plotly.express as px

data_im = import_data('csv','sales.csv')
data_cl = process_data(data_im)

print(data_cl.columns)


#make clealry that these infernces are auto,not analiticaly

def mean_ticket_month(data: pd.DataFrame):

    total_revenue = data.groupby('Month')['price'].agg('sum') / data.groupby('Month')['client_id'].agg('count')
    data = pd.DataFrame({'Month':total_revenue.index,'Revenue':list(total_revenue)})

    fig = px.line(data,x='Month',y='Revenue',title='Average Ticket Price per Month')
    fig.show()


#### stats,prob and tests

#close to the pop mean
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


#decorator
def determine_the_normality_of_data_for_tests(data: pd.DataFrame,col: str) -> dict:

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


def poisson_prob_for_sales_and_quantity(data: pd.DataFrame,range: str) -> float:
    '''Decriptive assumption: 
    these probabilities here are totally based descriptive statistics about the data'''

    #price in day-> prob sell S in 1 month
    data['revenue_day'] =  data.groupby('Day')['price'].agg('sum')
    mean_revenue_day = data['revenue_day'].mean()
    dist_revenue = poisson.cdf(range,mean_revenue_day)

    data['qtd_day'] =  data.groupby('Day')['quantity'].agg('sum')
    mean_solds_day = data['qtd'].mean()
    dist_qtd = poisson.cdf(range,mean_solds_day)

    #exponential: time for sale n

    return data




def prob_sell_specific_product_sector(data,product: str):
    #use binomial

    #filters
    return data


def product_sales_differences(data: pd.DataFrame):

    return data