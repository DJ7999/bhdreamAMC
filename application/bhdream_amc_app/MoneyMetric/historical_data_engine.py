import yfinance as yf
from datetime import datetime, timedelta

def get_dates():
    today = datetime.now()
    ten_years_ago = today - timedelta(days=365*10)
    
    today_str = today.strftime('%Y-%m-%d')
    ten_years_ago_str = ten_years_ago.strftime('%Y-%m-%d')
    
    return today_str, ten_years_ago_str

def apply_extension_to_symbol(symbol_list):
    return [symbol + ".NS" if not symbol.endswith(".NS") else symbol for symbol in symbol_list]

def get_historical_data(symbol_list):
    symbol_list=apply_extension_to_symbol(symbol_list)
    start_date, end_date=get_dates()
    historical_data=yf.download(tickers=symbol_list,start=start_date,end=end_date,interval="1mo")
    return historical_data

