from src.Inference.optimization import product_sale_optimization
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data
from src.app.app import load_data


def test_sales_optimization(data_format_path):

    data_imp = import_data(data_format_path[0],data_format_path[1])
    data_pr = process_data(data_imp)
    data1 = load_data(data_pr)


    data = data1.groupby('product_name',as_index=False).agg(
    price = ('price','mean'))

    prices = {data.loc[i,'product_name']: float(data.loc[i,'price']) for i in data.index}
    costs = {data.loc[i,'product_name']: float(data['price'].mean()) for i in data.index}
    capacity_weight = {data.loc[i,'product_name']: 10 for i in data.index}
    total_capacity =  {data.loc[i,'product_name']: 500 for i in data.index}
    budget = 50000

    results = product_sale_optimization(data,prices,costs,capacity_weight,total_capacity,budget)

    keys = {'status','Variables','Objective(max)'}
    assert keys.issubset(results.keys())

    assert results['status'] in ['Optimal','Infeasible','Unbounded','Not Solved','Undefined']

    for product,quantity in results['Variables']['quantity'].items():
        assert quantity >= 0