import requests 
import pandas as pd
from pandas import read_csv

from app.alpha_service import API_KEY

def fetch_stocks_csv(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
    df = read_csv(request_url)
    print(df)
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype("string"))
    return df
