from src.Inference.forecasting import plot_arima_graphs,forecast_arima
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app.app import load_data

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib
matplotlib.use('Agg')

def test_plot_arima(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data = load_data(data_pr)


    data = pd.DataFrame({
                        'datetime': data['datetime'],
                        'series': data['revenue'].astype(int)
                    })
            
    data = data.groupby('datetime',as_index=True)['series'].sum()
    data.index = pd.to_datetime(data.index)

    results = plot_arima_graphs(data)

    assert len(results['figs']) == 4

    for fig in results['figs']:
        assert isinstance(fig,matplotlib.figure.Figure)

    plt.close('all')


def test_arima(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data = load_data(data_pr)

    data = pd.DataFrame({
                        'datetime': data['datetime'],
                        'series': data['revenue'].astype(int)
                    })
            
    data = data.groupby('datetime',as_index=True)['series'].sum()
    data.index = pd.to_datetime(data.index)

    results = forecast_arima(data)

    keys = {'figs','summary','metrics'}
    assert keys.issubset(results.keys())
