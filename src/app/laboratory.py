import streamlit as st
import pandas as pd
import streamlit as st
from data_loading.importing import import_data
from data_loading.processing import process_data
from app import load_data,apply_filters


import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from Inference.forecasting import forecast_arima,plot_arima_graphs
from Inference.optimization import product_sale_optimization


st.markdown('Laboratoy')
st.sidebar.markdown('Laboratory')


def main():
    st.header('Forecast,Optimization and Statistics')

    df = import_data('csv','sales4.csv')
    df = process_data(df)

    df = load_data(df)
    df = apply_filters(df)

    data_fr = df


    datetime_type = st.sidebar.selectbox('Select datetime metric: ',['month','datetime'])
    if datetime_type == 'datetime':
        lags = 7
        period = 7
    else: 
        period = 12
        lags = 12

    plt.clf()
    st.dataframe(df.head())


    tab1,tab2,tab3 = st.tabs(['Series Diagnostics','Model Selection and Forecast','Optimization'])

    with tab1:

        results = plot_arima_graphs(data_fr,lags,period,datetime_type)
        fig1,fig2,fig3,fig4 = results['figs'][0],results['figs'][1],results['figs'][2],results['figs'][3]

        #diff analyst


        #correlation and seasonality
        col1,col2,col3 = st.columns(3)

        with col1:
            st.pyplot(fig1)
            
        with col2:
            st.pyplot(fig2)

        with col3:
            st.pyplot(fig3)

        st.pyplot(fig4)

    with tab2:


        test = results['test']
        st.metric('AdFuller Test p_value: ', test[1])
        st.write(test)
        

        ar = st.number_input(label='Ar lag',value=1,key='ar')
        ma = st.number_input(label='Ma lag',value=1,key='ma')
        diff = st.number_input(label='Diff lag',value=0,key='diff')

        model = (ar,diff,ma)
        steps = st.number_input(label='steps',value=10,key='step')

        results = forecast_arima(data_fr,datetime_type,steps,model,)

        fig = results['figs']
        st.pyplot(fig)


        #metrics:
        col1,col2 = st.columns(2)
        
        col1.metric('Aic: ', results['metrics']['AIC'])
        col2.metric('Bic: ', results['metrics']['BIC'])

        st.write(results['summary'])

        #evals:

    with tab3:

        data_op = df

        cost1 = df['price'].mean()
        costs = {}
        capacity_weight = {}
        total_capacity = {}

        products = df['product_name'].unique()
    
        with st.expander('Product params'):
            for product in products:
                col1,col2,col3 = st.columns(3)
                with col1:
                    costs[product] = st.number_input(f'Cost : {product}', value=cost1, key=f'cost_{product}')
                with col2:
                    capacity_weight[product] = st.number_input(f'Capacity Size: {product}', value=10.0, key=f'capacity_{product}')
                with col3:
                    total_capacity[product] = st.number_input(f'Capacity Limit{product}', value=500, key=f'stock_limit_{product}')

        budget = st.number_input('Budget: ',value=50000,key='budget')

        results = product_sale_optimization(data_op,costs,capacity_weight,total_capacity,budget)

        st.header('Results')

        col1,col2,col3 = st.columns(3)

        col1.metric('Model status', results['status'])
        col2.metric('Total profit', results['Objective(max)'])


        datag = pd.DataFrame({'product':results['Variables']['quantity'].keys(),
                        'quantity':results['Variables']['quantity'].values(),
                        'prices':results['Variables']['price'].values()})
        st.dataframe(datag)

        col4,col5 = st.columns(2)

        with col4:
            st.bar_chart(datag.set_index('product')['quantity'])

            
if __name__ == "__main__":
    main()
