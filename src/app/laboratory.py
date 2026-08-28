import streamlit as st
import pandas as pd
from data_loading.importing import import_data
from data_loading.processing import process_data
from app import load_data,apply_filters


import matplotlib.pyplot as plt
from src.Inference.forecasting import forecast_arima,plot_arima_graphs
from Inference.optimization import product_sale_optimization
from Inference.statistics import (
    determine_the_normality_of_data,
    mean_ticket_month,
    chi_square_tests,
    prob_quantity_per_time,
    prob_revenue_per_time,
    prob_sell_specific_product_sector
)
st.sidebar.markdown('Laboratory')


def main():
    st.title('🔬 Sales Inference')

    df = import_data('csv','sales4.csv')
    df = process_data(df)

    df = load_data(df)
    df = apply_filters(df)


    tab1,tab2,tab3,tab4 = st.tabs(['📊 Data Statistics','📄 Series Diagnostics',
                                '📈 Model Selection and Forecast','📌 Optimization'])

    with tab1:

        data_stats = df

        tab_numbers,tab_products = st.tabs(['Price and quantity','Products and Probability'])

        with tab_numbers:
            mean_ticket = mean_ticket_month(data_stats)
            st.plotly_chart(mean_ticket)
        

            st.write('Price normality')

            results_normality1 = determine_the_normality_of_data(data_stats,col='price')

            col1,col2 = st.columns(2)
            col1.metric('Skew Stat', results_normality1['skew'])
            col2.metric('Shapiro p_val', results_normality1['shapiro'])

            col3,col4 = st.columns(2)
            col3.metric('Kurtosis stat', results_normality1['kurtosis'])
            col4.metric('Recommended Test: ', results_normality1['test'])

            st.plotly_chart(results_normality1['fig'])

            st.write('Quantity normality')
            
            results_normality2 = determine_the_normality_of_data(data_stats,col='quantity')

            col1,col2 = st.columns(2)
            col1.metric('Skew Stat', results_normality2['skew'])
            col2.metric('Shapiro p_val', results_normality2['shapiro'])

            col3,col4 = st.columns(2)
            col3.metric('Kurtosis stat', results_normality2['kurtosis'])
            col4.metric('Recommended Test: ', results_normality2['test'])

            st.plotly_chart(results_normality2['fig'])

        with tab_products:

            results_chi_square = chi_square_tests(data_stats,col='product_name')
            col1,col2 = st.columns(2)

            col1.metric('ChiSquare Goodness-of-Fit Stat', results_chi_square[0])
            col2.metric('ChiSquare Goodness-of-Fit P-Value', results_chi_square[1])




#update: continuous and categorial tests-prob

    with tab2:

        data_fr = df
        
        datetime_type = st.sidebar.selectbox('Select datetime metric: ',['month','datetime'])
        if datetime_type == 'datetime':
            lags = 7
            period = 7
        else: 
            period = 12
            lags = 12
    
        plt.clf()
        df1 = df.groupby(datetime_type)['revenue'].sum()
    
        st.dataframe(df1.head(5))

        results_graphs = plot_arima_graphs(data_fr,lags,period,datetime_type)
        fig1,fig2,fig3,fig4 = results_graphs['figs'][0],results_graphs['figs'][1],results_graphs['figs'][2],results_graphs['figs'][3]

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

    with tab3:


        test = results_graphs['test']
        st.metric('AdFuller Test p_value: ', test[1])
        st.write(test)
        

        ar = st.number_input(label='Ar lag',value=1,key='ar')
        ma = st.number_input(label='Ma lag',value=1,key='ma')
        diff = st.number_input(label='Diff lag',value=0,key='diff')

        model = (ar,diff,ma)
        steps = st.number_input(label='steps',value=10,key='step')

        results_arima = forecast_arima(data_fr,datetime_type,steps,model,)

        cola,colb = st.columns(2)
        fig_results,fig_diagnostics  = results_arima['figs'][0],results_arima['figs'][1]

        with cola:
            st.pyplot(fig_results)
            plt.close(fig_results)

        with colb:
            st.pyplot(fig_diagnostics)
            plt.close(fig_diagnostics)


        #metrics:
        col1,col2 = st.columns(2)
        
        col1.metric('Aic: ', results_arima['metrics']['AIC'])
        col2.metric('Bic: ', results_arima['metrics']['BIC'])

        st.write(results_arima['summary'])

        #evals:

    with tab4:

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

        results_optimization = product_sale_optimization(data_op,costs,capacity_weight,total_capacity,budget)

        st.header('Results')

        col1,col2,col3 = st.columns(3)

        col1.metric('Model status', results_optimization['status'])
        col2.metric('Total profit', results_optimization['Objective(max)'])


        datag = pd.DataFrame({'product':results_optimization['Variables']['quantity'].keys(),
                        'quantity':results_optimization['Variables']['quantity'].values(),
                        'prices':results_optimization['Variables']['price'].values()})
        st.dataframe(datag)

        col4,col5 = st.columns(2)

        with col4:
            st.bar_chart(datag.set_index('product')['quantity'])

            
if __name__ == "__main__":
    main()
