from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import pandas as pd

from statsmodels.tsa.stattools import adfuller

import matplotlib
matplotlib.use('Agg')


def plot_arima_graphs(data: pd.DataFrame,lags: int,period: int,datetime_type: str) -> dict:


    data = pd.DataFrame({
                            'datetime': data[datetime_type],
                            'series': data['revenue'].astype(int)
                        })
                
    data = data.groupby('datetime',as_index=True)['series'].sum()
    data.index = pd.to_datetime(data.index)


    fig1, ax1 = plt.subplots()
    ax1.plot(data,color='red',label='data')

    fig2,ax2 = plt.subplots()
    plot_acf(data,lags=lags,alpha=0.05,ax=ax2)
    

    fig3,ax3 = plt.subplots()
    plot_pacf(data,lags=lags,alpha=0.05,ax=ax3)


    sea = seasonal_decompose(x=data,period=period)
    fig4 = sea.plot()

    adfuller_test = adfuller(data)

    return {'figs': [fig1,fig2,fig3,fig4],'test': adfuller_test}


def forecast_arima(data: pd.DataFrame,datetime_type: str,steps: int = 20,model: tuple = (1,0,1)) -> dict:


    data = pd.DataFrame({
                                'datetime': data[datetime_type],
                                'series': data['revenue'].astype(int)
                            })
                    
    data = data.groupby('datetime',as_index=True)['series'].sum()
    data.index = pd.to_datetime(data.index)

    #predicts
    if model[1] != 0:
        model = ARIMA(data,order=model)
        
    else:
        model = ARIMA(data,order=model)
        

    model = model.fit()

    #results_predicts = model.get (steps=steps)
    results_forecast = model.get_forecast(steps=steps)

    #predicts = results_predicts.predicted_mean
    forecast = results_forecast.predicted_mean

    #predict_int = results_predicts.conf_int()
    forecast_int = results_forecast.conf_int()

    #evaluate
    metrics = {'AIC': model.aic,'BIC':model.bic}
    summary = model.summary()

    #ax1,fig1 = plt.subplots()
    #plt.plot(predicts.index,predicts,color='blue',label='predicts')

    #plt.fill_between(
    #predict_int.index,
    #predict_int.iloc[:, 0],
    #predict_int.iloc[:, 1],
    #color='blue',
    #alpha=0.2,
    #label='Conf Int'
    #)

    data.index = pd.to_datetime(data.index)
    #forecast.index = pd.to_datetime(forecast.index)
    #forecast_int = pd.to_datetime(forecast_int.index)

    plt.clf()


    new_data = data.index.max()
    data_r = pd.date_range(
        start = new_data,periods=steps + 1
    )[1:]

    forecast.index = data_r
    forecast_int.index = data_r

    fig2,ax2 = plt.subplots()
    ax2.plot(data.index,data,color='red',label='data')
    ax2.plot(forecast.index,forecast,color='blue',label='forecast')
    plt.fill_between(
        forecast_int.index,
        forecast_int.iloc[:, 0],
        forecast_int.iloc[:, 1],
        color='blue',
        alpha=0.2,
        label='Conf Int'
        )
    plt.legend()

    
    fig3 = model.plot_diagnostics()
    plt.show()

    return {'figs': [fig3,fig2],'summary':summary,'metrics':metrics}
