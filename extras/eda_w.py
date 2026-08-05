import json
import streamlit as st
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

data_w = pd.read_csv('/home/augusto2/Sales_inteligence_dh-api/extras/Zenless Zone Zero Measurements 3.1 - measurements.csv').drop('Notes',axis=1)
print(data_w.head,data_w.dtypes)

#streamlit
st.markdown(" Main Page")
st.sidebar.markdown('Main Page')

st.title('Waifus Analyst 😎')
data_df,graphs = st.tabs(['dataframe','Graphs'])

##graphs:

with data_df:

    st.header('Waifus dataframe')
    if st.checkbox("show data"):
            side = st.sidebar.slider('height',min_value=0,max_value=200)
            st.dataframe(data_w.loc[data_w['cm']> side])

    #filters
    st.header('Select height max range')
    s = st.slider('height',min_value=0,max_value=200)

    st.dataframe(data_w.loc[data_w['cm']> s])

    #compare data
    st.header('Compare waifus')
    st.text_input('waifu name here: ',key='w_name')
    st.dataframe(data_w.loc[data_w['Character'] == st.session_state.w_name])

    ww = st.selectbox('What waifus do you want to compare?',data_w['Character'])
    cols = st.radio('select columns to compare',(data_w.columns))
    st.dataframe(data_w.loc[data_w['Character'] == ww,cols])


    r,l = st.columns(2)
    r.button('right label')
    l.button('left label')

    if st.button('sort'):
        e = st.radio('sorting w',('1','2','3'))
        st.write(f'you chose: {e}')

    with l:
        st.radio('sorting w',('11','34','32'))


import time
with graphs:
    st.header('Waifus Height')
    st.bar_chart(data_w,x='Character',y='cm')

    #map_data = pd.DataFrame(
    #np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    #columns=['lat', 'lon'])
    #st.map(map_data)
    cont = st.empty()
    tim = st.progress(0)

    for i in range(100):
        cont.text(f'loading %{i}')
        tim.progress(i + 1)
        #not instantly:
        time.sleep(0.1)
    st.header('Proccess Completed!!')
         
    
