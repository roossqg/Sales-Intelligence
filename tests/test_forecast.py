from src.Inference.forecasting import plot_arima_graphs
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app import load_data

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def test_plot_arima(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data = load_data(data_pr)

    plot_arima_graphs(data,col='revenue',time_period='month')
    plt.close('all')
