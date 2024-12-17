import requests 
import pandas as pd
from datetime import datetime, timedelta
from pandas import read_csv

from app.alpha_service import API_KEY

def fetch_stocks_csv(symbol, time):
    # fetching data from AlphaVantage
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
    df = read_csv(request_url)
        
    # convert timestamp column into datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype("string"))
    
    # only get timestamp and adjusted_close
    df = df[['timestamp','adjusted_close']]

    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    print(type(today))

    m = int(time)

    # converting time from radio button into number of months (m)
    '''if time == "1M": m = 1
    if time == "6M": m = 6
    if time == "1Y": m = 12
    if time == "5Y": m = 60   ''' 

    # Calculate the offset
    m_months_ago = today - pd.DateOffset(months=m)

    # filtering the data till m months ago
    df = df[(df['timestamp'] >= m_months_ago) & (df['timestamp'] <= today)]

    return df
