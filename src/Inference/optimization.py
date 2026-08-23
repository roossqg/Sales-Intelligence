import pulp


def product_sale_optimization(data,prices,costs,capacity_weight,total_capacity,budget): 

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

     