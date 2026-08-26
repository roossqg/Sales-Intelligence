from src.Inference.optimization import product_sale_optimization

def test_sales_optimization(data_full):

    data = data_full

    prices = {data.loc[i,'product_name']: float(data.loc[i,'price']) for i in data.index}
    costs = {data.loc[i,'product_name']: float(data['price'].mean()) for i in data.index}
    capacity_weight = {data.loc[i,'product_name']: 10 for i in data.index}
    total_capacity =  {data.loc[i,'product_name']: 500 for i in data.index}
    budget = 50000

    results = product_sale_optimization(data,costs,capacity_weight,total_capacity,budget)

    keys = {'status','Variables','Objective(max)'}
    assert keys.issubset(results.keys())

    assert results['status'] in ['Optimal','Infeasible','Unbounded','Not Solved','Undefined']

    for product,quantity in results['Variables']['quantity'].items():
        assert quantity >= 0