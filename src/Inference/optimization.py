import pulp
import pandas as pd
from src.data_loading.importing import import_data
from src.data_loading.processing import process_data

data_i = import_data('csv','sales.csv')
data_p = process_data(data_i)

##product opt

#define problems-funcs:



def product_sale_optimization():

    # price x quat
    model = pulp.LpProblem('Best price-qtd',pulp.LpMaximize)

    #price = pulp.LpVariable('price',lowBound=20,upBound=,cat='Integer')

    #fix:
    price = 40 
    discount = pulp.LpVariable('price',lowBound=0,upBound=None,cat='Integer')
    quantity = pulp.LpVariable('quantity',lowBound=0,upBound=None,cat='Integer')

    model += (price - discount)  * quantity
    model.solve()

    results = {
        'status': pulp.LpStatus[model.status],
        'Variables': {'quantity': quantity.varValue},
        'Objective(max)': pulp.value(model.objective)
    }

    return results

    #return best price-qtd given budget,capacity and minimum demand


def plan_stock():

def price_opt()

def plan_cat():

print(product_sale_optimization())

