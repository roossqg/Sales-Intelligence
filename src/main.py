import streamlit as st

page1 = st.Page(page='app.py',title='Dashboard')
page2 = st.Page(page='predicts.py',title='Laboratory')


pg = st.navigation([page1,page2],position='sidebar')

pg.run()

