from src.Inference.forecasting import plot_arima_graphs,forecast_arima
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app.app import load_data

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib
matplotlib.use('Agg')

def test_plot_arima(data_full):

    data = data_full

    results = plot_arima_graphs(data,lags=7,period=7,datetime_type='datetime')

    assert len(results['figs']) == 4

    for fig in results['figs']:
        assert isinstance(fig,matplotlib.figure.Figure)

    plt.close('all')


def test_arima(data_full):

    data = data_full

    results = forecast_arima(data,'datetime')

    keys = {'figs','summary','metrics'}
    assert keys.issubset(results.keys())
