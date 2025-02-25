from backend.utils.database import engine
import pandas as pd


class StatResource:
    path = ''
    
    @staticmethod
    def read_data_from_query(query):
        return pd.read_sql(query.statement, engine)
    
    @staticmethod 
    def to_datetime(col):
        return pd.to_datetime(col)
    
    @staticmethod 
    def to_timestamp(x):
        return pd.Timestamp(x).timestamp()*1000
  