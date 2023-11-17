from portfolio_controller.models import Equity  # Import the EquitySymbol model

class EquityDTO:
    # def __init__(self, equity_symbol, amount_invested):
    #     self.equity_symbol = equity_symbol  # equity_symbol should be an instance of EquitySymbol
    #     self.amount_invested = amount_invested
    #     self.cagr = None
    #     self.risk = None
    #     self.optimal_weight=None
    
    def __init__(self, equity_symbol, amount_invested, cagr=None, risk=None, optimal_weight=None):
        self.equity_symbol = equity_symbol
        self.amount_invested = amount_invested
        self.cagr = cagr
        self.risk = risk
        self.optimal_weight = optimal_weight

    def get_equity_symbol(self):
        return self.equity_symbol

    def get_cagr(self):
        return self.cagr

    def get_risk(self):
        return self.risk
    
    def set_cagr(self, cagr):
        self.cagr = cagr

    def set_risk(self, risk):
        self.risk = risk
    
    def set_optimal_weight(self, optimal_weight):
        self.optimal_weight = optimal_weight

class PortfolioDTO:
    def __init__(self, equity_data_list=None):
        self.equities = equity_data_list  # equities should be a list of EquityDTO instances
        self.has_metrics = False
        self.is_optimised=False
        self.current_return=None
        self.current_risk=None
        self.optimised_return=None
        self.optimised_risk=None
        self.total_portfolio_value=sum(equity.amount_invested for equity in equity_data_list) if  equity_data_list is not None else None

    def get_equities(self):
        return self.equities
    
    def set_equities(self,equities):
        self.equities=equities

    def set_optimised_return(self,optimised_return):
        self.optimised_return=optimised_return
    
    def set_optimised_risk(self,optimised_risk):
        self.optimised_risk=optimised_risk

    def set_current_return(self,current_return):
        self.current_return=current_return
    
    def set_current_risk(self,current_risk):
        self.current_risk=current_risk

    def get_equity_symbols(self):
        return [equity.get_equity_symbol() for equity in self.equities]
    
    def Enable_metrics(self):
        self.has_metrics=True

    def Is_metrics_Enable(self):
        return self.has_metrics
    
    def get_cagrs(self):
        return [equity.get_cagr() for equity in self.equities]
    
    def get_risks(self):
        return [equity.get_risk() for equity in self.equities]

    def get_equity(self, equity_symbol):
        for equity in self.equities:
            if equity.get_equity_symbol() == equity_symbol:
                return equity
        # If equity_symbol is not found, you can return None or raise an exception
        return None
    
    def get_total_portfolio_value(self):
        return self.total_portfolio_value
    
    def set_cagrs(self, cagr_updates):
        for update in cagr_updates:
            equity_symbol = update.key
            new_cagr = update.value
            for equity in self.equities:
                if equity.get_equity_symbol() == equity_symbol:
                    equity.set_cagr(new_cagr)
                    break
    
    def set_risks(self, risk_updates):
        for update in risk_updates:
            equity_symbol = update.key
            new_cagr = update.value
            for equity in self.equities:
                if equity.get_equity_symbol() == equity_symbol:
                    equity.set_risk(new_cagr)
                    break

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.equities = [EquityDTO(**equity_data) for equity_data in data.get('equities', [])]
        instance.has_metrics = data.get('has_metrics', False)
        instance.is_optimised = data.get('is_optimised', False)
        instance.current_return = data.get('current_return')
        instance.current_risk = data.get('current_risk')
        instance.optimised_return = data.get('optimised_return')
        instance.optimised_risk = data.get('optimised_risk')
        instance.total_portfolio_value = data.get('total_portfolio_value')
        return instance
    
class KeyValuePairDTO:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"Key: {self.key}, Value: {self.value}"
