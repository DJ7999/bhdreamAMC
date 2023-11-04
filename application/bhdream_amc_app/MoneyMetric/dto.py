from user_controller.models import EquitySymbol  # Import the EquitySymbol model

class EquityDTO:
    def __init__(self, equity_symbol, amount_invested):
        self.equity_symbol = equity_symbol  # equity_symbol should be an instance of EquitySymbol
        self.amount_invested = amount_invested

    def get_equity_symbol(self):
        return self.equity_symbol

class PortfolioDTO:
    def __init__(self, equity_data_list):
        self.equities = equity_data_list  # equities should be a list of EquityDTO instances
    
    def get_equity_symbols(self):
        return [equity.get_equity_symbol() for equity in self.equities]
