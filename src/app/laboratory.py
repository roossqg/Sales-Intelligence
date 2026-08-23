import streamlit as st
import pandas as pd
import streamlit as st
from data_loading.importing import import_data
from data_loading.processing import process_data
from src.app.app import load_data,apply_filters

from statsmodels.tsa.stattools import adfuller

import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from Inference.forecasting import forecast_arima,plot_arima_graphs
from Inference.optimization import product_sale_optimization

from src.data_loading.data_flow import export_data_sql,get_data_sql

st.markdown('Forecast and Optimization')
st.sidebar.markdown('Forecast and Optimization')


def main():
    st.header('forecast')


    df = import_data('csv','sales4.csv')
    df = process_data(df)

    df = export_data_sql('csv','sales4.csv')
    df = get_data_sql()

    df = load_data(df)
    df = apply_filters(df)


    datetime_type = st.sidebar.selectbox('Select datetime metric: ',['month','datetime'])
    if datetime_type == 'datetime':
        lags = 7
        period = 7
    else: 
        period = 12
        lags = 12

    data_fr = pd.DataFrame({
                    'datetime': df[datetime_type],
                    'series': df['revenue'].astype(int)
                })
        
    data = data_fr.groupby('datetime',as_index=True)['series'].sum()
    data_fr.index = pd.to_datetime(data_fr.index)
    plt.clf()
    st.dataframe(data_fr.head())


    tab1,tab2,tab3 = st.tabs(['Series Diagnostics','Model Selection and Forecast','Optimization'])

    with tab1:

        col1,col2,col3 = st.columns(3)


        with col1:
            fig1,ax1 = plt.subplots()
            ax1.plot(data_fr,color='red',label='data')
            st.pyplot(fig1)
            

        #ar,ma,armax
        with col2:
            fig2,ax2 = plt.subplots()
            plot_acf(data_fr,lags=lags,alpha=0.05,ax=ax2)
            st.pyplot(fig2)

        with col3:
            fig3,ax3 = plt.subplots()
            plot_pacf(data_fr,lags=lags,alpha=0.05,ax=ax3)
            st.pyplot(fig3)

        fig4 , ax4 = plt.subplots()
        sea = seasonal_decompose(data_fr,period=period)
        fig_sea = sea.plot()
        st.pyplot(fig_sea)

    with tab2:

        test = adfuller(data_fr)
        st.metric('AdFuller Test p_value: ', test[1])
        

        ar = st.number_input(label='Ar lag',value=1,key='ar')
        ma = st.number_input(label='Ma lag',value=1,key='ma')
        diff = st.number_input(label='Diff lag',value=0,key='diff')

        model = (ar,diff,ma)
        steps = st.number_input(label='steps',value=10,key='step')

        results = forecast_arima(data_fr,steps,model,p='d')

        fig = results['figs']
        st.pyplot(fig)

    with tab3:

        data_op = df.groupby('product_name',as_index=False).agg(
            price = ('price','mean'))

        prices = {data_op.loc[i,'product_name']: float(data_op.loc[i,'price']) for i in data_op.index}

        cost1 = df['price'].mean()
        costs = {}
        capacity_weight = {}
        total_capacity = {}

        products = df['product_name'].unique()
    

        with st.expander('Product params'):
            for product in products:
                col1,col2,col3 = st.columns(3)
                with col1:
                    costs[product] = st.number_input(f'Cost : {product}', value=cost1, key=f'cost_{product}')
                with col2:
                    capacity_weight[product] = st.number_input(f'Capacity Size: {product}', value=10.0, key=f'capacity_{product}')
                with col3:
                    total_capacity[product] = st.number_input(f'Capacity Limit{product}', value=500, key=f'stock_limit_{product}')

        
        budget = 50000

        results = product_sale_optimization(data_op,prices,costs,capacity_weight,total_capacity,budget)

        st.header('Results')

        col1,col2,col3 = st.columns(3)

        col1.metric('Model status', results['status'])
        col2.metric('Total profit', results['Objective(max)'])


        datag = pd.DataFrame({'product':results['Variables']['quantity'].keys(),
                        'quantity':results['Variables']['quantity'].values(),
                        'prices':results['Variables']['price'].values()})
        st.dataframe(datag)

        col4,col5 = st.columns(2)

        with col4:
            st.bar_chart(datag.set_index('product')['quantity'])

            

if __name__ == "__main__":
    main()
