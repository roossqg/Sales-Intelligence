import pulp
import pandas as pd
from data_loading.importing import import_data
from data_loading.processing import process_data

data_i = import_data('csv','sales4.csv')
data_p = process_data(data_i)
data = data_p.groupby('product_name',as_index=False).agg(
    price = ('price','mean')
)

prices = {data.loc[i,'product_name']: data['price'].mean() for i in data.index}
bud = data['price'].sum()
capacity_weight = {data.loc[i,'product_name']: 10 for i in data.index}


##product opt

#define problems-funcs:


#limits: price limits and qtd limits
#constraints: 1.budget per product,2.capacity per product,3.category min/max
def product_sale_optimization(data,prices,costs,capacity_weight,total_capacity,budget): 

    #data:
    products = data['product_name'].unique()

    data = data_i.groupby('product_name',as_index=False).agg(
    price = ('price','mean')
)

    #total_capacity = 15000

    # price x quat
    model = pulp.LpProblem('profit maximization',pulp.LpMaximize)

    quantity = pulp.LpVariable.dicts('quantity',products,lowBound=0,upBound=None,cat='Integer')
    
 
    #model += (prices * quantity) - (costs * quantity) #profit
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


#limits: price limits,demand model(datetime,qtd,price)
#constraints: 1.conf interval
#def price_opt()

#dataf = product_sale_optimization(data_p)
#datag = pd.DataFrame({'product':dataf['Variables']['quantity'].keys(),
                      #'quantity':dataf['Variables']['quantity'].values()})


#print(datag['quantity'].value_counts())