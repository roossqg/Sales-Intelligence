from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.tsatools import adfuller
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import pandas as pd
import streamlit as st


#times periods + (qtd,revenue)
#groups per category,age,products
#conf interval + plots + evaluate-compare
#cautions of less sales

#plot eavluations for confidence

def plot_arima_graphs(data,col,time_period):
    #plot series of respective time series
    plt.plot(y=data[col],x=data[time_period],color='red',label='data')

    #ar,ma,armax
    plot_acf(data[col],lags=20,alpha=0.05)
    plot_pacf(data[col],lags=20,alpha=0.05)

    sea = seasonal_decompose(x=data[time_period],y=data[col])
    sea.plot()

    plt.show()


def forecast_arima(time_period,predict_range,steps,col,data: pd.data,model: tuple):

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

