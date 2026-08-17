from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import pandas as pd
import streamlit as st


#from app import load_data
import matplotlib
matplotlib.use('Agg')

#times periods + (qtd,revenue)
#groups per category,age,products
#conf interval + plots + evaluate-compare
#cautions of less sales

#plot eavluations for confidence

def plot_arima_graphs(data,col,time_period):
    #plot series of respective time series

    data = pd.DataFrame({
        'datetime': data[time_period],
        'series': data[col]
    })

    data = data.set_index('datetime')

    fig1, ax1 = plt.subplots()

    ax1.plot(data,color='red',label='data')
    st.pyplot(fig1)
    

    #ar,ma,armax
    fig2,ax2 = plt.subplots()
    plot_acf(data,lags=20,alpha=0.05,ax=ax2)
    

    fig3,ax3 = plt.subplots()
    figplot_pacf(data,lags=20,alpha=0.05,ax=ax3)


    #sea = seasonal_decompose(x=data[col])
    #sea.plot()


def forecast_arima(time_period,predict_range,steps,col,data,model: tuple):

    test = adfuller(data[col])
    st.metric('adfuller: ',test)
    st.text_input('Select model: ',key='model')
    model = st.session_state.model


    #predicts
    if model[1] != 0:
        model = ARIMA(x=data[time_period],y=data[col],order=model,exog=model[4]).fit()
    else:
        model = ARIMA(x=data[time_period],y=data[col],order=model).fit()

    results_predicts = model.get_predictions(steps=steps)
    results_forecast = model.get_forecast(steps=steps)

    predicts = results_predicts.predictions_mean
    forecast = results_forecast.predictions_mean

    predict_int = results_predicts.conf_int()
    forecast_int = results_forecast.conf_int()

    #evaluate
    metrics = {'AIC': model.aic,'BIC':model.bic}
    summary = model.summary()

    plt.plot(predicts.index,predicts,color='blue',label='predicts')

    plt.fill_between(
    predict_int.index,
    predict_int.iloc[:, 0],
    predict_int.iloc[:, 1],
    color='blue',
    alpha=0.2,
    label='Conf Int'
    )
    
    plt.plot(forecast.index,forecast,color='blue',label='forecast')
    plt.fill_between(
        forecast_int.index,
        forecast_int.iloc[:, 0],
        forecast_int.iloc[:, 1],
        color='blue',
        alpha=0.2,
        label='Conf Int'
        )

    plt.legend()
    plt.show()


    return metrics
