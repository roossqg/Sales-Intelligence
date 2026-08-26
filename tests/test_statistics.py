from src.Inference.statistics import mean_ticket_month,determine_the_normality_of_data,chi_square_tests
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app.app import load_data
import plotly.express as px
from plotly.graph_objects import Figure
import matplotlib
matplotlib.use('Agg')


def test_mean_ticket(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data1 = load_data(data_pr)

    results = mean_ticket_month(data1)

    assert isinstance(results,Figure)


def test_normality_of_data(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data1 = load_data(data_pr)

    results = determine_the_normality_of_data(data1,col='quantity')

    keys = {'skew','shapiro','kurtosis','test'}
    assert keys.issubset(results.keys())

    assert results['shapiro'] <= 1
    assert results['kurtosis'] <= 1


def test_chi_square(data_format_path):
    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data1 = load_data(data_pr)

    results = chi_square_tests(data1,col='product_name')

    assert results <= 1
