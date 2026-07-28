#from load_data import export_sql_to_csv

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px

matplotlib.use('QtAgg')

import streamlit as st

#data = export_sql_to_csv()
data = pd.read_csv('sales.csv')

######## most sale cat


st.title("📊 Sales per Sector")


fig = px.bar(data, y="category", x="quantity", orientation="h")
st.plotly_chart(fig, use_container_width=True)


## sale pr per sector




## linegraph with sales per month




