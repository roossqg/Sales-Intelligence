import pulp
import pandas as pd
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data

data_i = import_data('csv','sales.csv')
data_p = process_data(data_i)

##product opt

#define problems-funcs:


#limits: price limits and qtd limits
#constraints: 1.budget per product,2.capacity per product,3.category min/max
def product_sale_optimization() -> variables for maximize: 

    # price x quat
    model = pulp.LpProblem('Best price-qtd',pulp.LpMaximize)

    #price = pulp.LpVariable('price',lowBound=20,upBound=,cat='Integer')

    #fix:
    price = pulp.LpVariable('price',lowBound=0,upBound=price_limits,cat='Float')
    quantity = pulp.LpVariable('quantity',lowBound=0,upBound=product_limits,cat='Integer')
 
    model += price * quantity

    #budget
    model += product_cost * quantity <= cost_limit


    #capacity
    model += sum(quantity) <= sum(product_capacity)  
    model += quantity <= product_capacity

    model.solve()

    results = {
        'status': pulp.LpStatus[model.status],
        'Variables': {'quantity': quantity.varValue,'price':price.varValue},
        'Objective(max)': pulp.value(model.objective)
    }

    return results

    


#limits: price limits,demand model(datetime,qtd,price)
#constraints: 1.conf interval
def price_opt()




print(product_sale_optimization())