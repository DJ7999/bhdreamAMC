import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def get_dates():
    today = datetime.now()
    ten_years_ago = today - timedelta(days=365*10)
    
    today_str = today.strftime('%Y-%m-%d')
    ten_years_ago_str = ten_years_ago.strftime('%Y-%m-%d')
    
    return  ten_years_ago_str,today_str

def get_historical_data(symbol_list):
    if len(symbol_list) == 0:
        return pd.DataFrame()
    start_date, end_date=get_dates()
    historical_data=yf.download(tickers=symbol_list,start=start_date,end=end_date,interval="1mo")
    if len(symbol_list) == 1:
        historical_data = historical_data[['Close']].rename(columns={'Close': symbol_list[0]})
        return historical_data
    return historical_data.Close

def get_latest_closing_price(symbol):
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')

    # Calculate the start date (10 days ago)
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

    # Download historical data for the last 10 days
    historical_data = yf.download(tickers=symbol, start=start_date, end=today_date)

    # Extract and return the closing price of the 10th day
    if not historical_data.empty and len(historical_data) >= 10:
        tenth_day_closing_price = historical_data['Close'].iloc[-1]
        return tenth_day_closing_price
    else:
        return None