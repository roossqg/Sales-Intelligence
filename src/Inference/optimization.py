import pulp


def product_sale_optimization(data,costs,capacity_weight,total_capacity,budget): 

    data_op = data.groupby('product_name',as_index=False).agg(
                price = ('price','mean'))
    
    prices = {data_op.loc[i,'product_name']: float(data_op.loc[i,'price']) for i in data_op.index}

    #data:
    products = data['product_name'].unique()

    model = pulp.LpProblem('profit_maximization',pulp.LpMaximize)

    quantity = pulp.LpVariable.dicts('quantity',products,lowBound=0,upBound=None,cat='Integer')
    
 
    model += pulp.lpSum((prices[i] * quantity[i]) - (costs[i] * quantity[i]) for i in products)

    model += pulp.lpSum(costs[i] * quantity[i] for i in products) <= budget

    for i in products:
        model += capacity_weight[i] * quantity[i] <= total_capacity[i]

    model.solve()

    results = {
        'status': pulp.LpStatus[model.status],
        'Variables': {'quantity': {i : quantity[i].varValue for i in  products},
                'price': {i : prices[i] for i in  prices.keys()}},
        'Objective(max)': pulp.value(model.objective)
    }

    return results

     