import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


page1 = st.Page(page='app.py',title='Dashboard')
page2 = st.Page(page='laboratory.py',title='Laboratory')


pg = st.navigation([page1,page2],position='sidebar')

pg.run()

