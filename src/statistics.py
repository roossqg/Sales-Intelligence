import pandas as pd


from data_loading.importing import import_data
from data_loading.processing import process_data

import plotly.express as px

data_im = import_data('csv','sales.csv')
data_cl = process_data(data_im)

print(data_cl.columns)


###

def calculate_ticket_month(data: pd.DataFrame):

    total_revenue = data.groupby('Month')['price'].agg('sum') / data.groupby('Month')['client_id'].agg('count')
    data = pd.DataFrame({'Month':total_revenue.index,'Revenue':list(total_revenue)})

    fig = px.line(data,x='Month',y='Revenue',title='Average Ticket Price per Month')
    fig.show()

    
