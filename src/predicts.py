import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
from data_loading.importing import import_data
from data_loading.processing import process_data
from app import load_data
from sqlite3 import connect

from statsmodels.tsa.stattools import adfuller

import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from Inference.forecasting import forecast_arima


st.markdown('Forecast and Optimization')
st.sidebar.markdown('Forecast and Optimization')


st.header('forecast')


df = import_data('csv','sales4.csv')
df = process_data(df)
df = load_data(df)

datetime_type = st.sidebar.selectbox('Select datetime metric: ',['month','year'])
if datetime_type == 'month':
    lags = 10
    period = 12
else: 
    period = 1
    lags = 1

data = pd.DataFrame({
                'datetime': df[datetime_type],
                'series': df['revenue'].astype(int)
            })
    
data = data.groupby('datetime',as_index=True)['series'].sum()


tab1,tab2 = st.tabs(['Series Dignostics','Model_selection'])

with tab1:

    #st.dataframe(data)

    col1,col2,col3 = st.columns(3)

    with col1:
        fig1,ax1 = plt.subplots()
        ax1.plot(data,color='red',label='data',marker='.')
        st.pyplot(fig1)
        

    #ar,ma,armax
    with col2:
        fig2,ax2 = plt.subplots()
        plot_acf(data,lags=lags,alpha=0.05,ax=ax2)
        st.pyplot(fig2)

    with col3:
        fig3,ax3 = plt.subplots()
        plot_pacf(data,lags=lags,alpha=0.05,ax=ax3)
        st.pyplot(fig3)

    fig4 , ax4 = plt.subplots()
    sea = seasonal_decompose(data,period=period)
    fig_sea = sea.plot()
    st.pyplot(fig_sea)

with tab2:

    test = adfuller(data)
    st.metric('adfuller p_value: ', test[1])
    #st.text_input('Select model: ',key='model')
    #model = st.session_state.model

    results = forecast_arima(data)

    fig = results['figs']
    st.pyplot(fig)
