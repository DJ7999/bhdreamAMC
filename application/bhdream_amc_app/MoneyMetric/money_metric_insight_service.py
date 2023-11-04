from historical_data_engine import get_historical_data

def get_metrics(portfolio):
    symbol_list=portfolio.get_equity_symbols()
    historical_data=get_historical_data(symbol_list).Close
    #calculate_metrics(historical_data)

#def calculate_metrics(historical_data):

