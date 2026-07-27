from database_create import engine
import pandas as pd


def export_sql(query='SELECT * FROM  sales'):

    df = pd.read_sql(query,engine)
    
