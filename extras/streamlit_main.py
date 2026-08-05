import streamlit as st

main_page = st.Page(page='eda_w.py',title='Eda',icon='👒',url_path='eda')
page_2 = st.Page(page='stats.py',title='Statistics',icon='🎓',url_path='statistics')
page_3 = st.Page(page='ml.py',title='Machine Learning',icon='🌂',url_path='ml_predict')

pg = st.navigation([main_page,page_2,page_3],position='top')

pg.run()