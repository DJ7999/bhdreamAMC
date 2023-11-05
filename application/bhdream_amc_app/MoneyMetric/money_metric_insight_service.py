from historical_data_engine import get_historical_data
from dto import KeyValuePairDTO
import numpy as np
from scipy.optimize import minimize

def populate_portfolio_metrics(portfolio):
    symbol_list=portfolio.get_equity_symbols()
    historical_data=get_historical_data(symbol_list).Close
    returns, risks  =calculate_metrics(historical_data)
    portfolio_return, portfolio_risk=current_portfolio_risk_return(portfolio.get_equities(),portfolio.get_total_portfolio_value())
    portfolio.set_cagrs(returns)
    portfolio.set_risks(risks)
    portfolio.Enable_metrics()
    portfolio.set_current_return(portfolio_return)
    portfolio.set_current_risk(portfolio_risk)
    return portfolio

def current_portfolio_risk_return(equity_list, total_portfolio_value):
    # Calculate the weights of each equity in the portfolio
    weights = [equity.amount_invested / total_portfolio_value for equity in equity_list]

    # Calculate the expected returns of each equity
    expected_returns = [equity.cagr for equity in equity_list]

    # Calculate the covariance matrix (assuming independent assets)
    risk_values = [equity.risk for equity in equity_list]
    cov_matrix = np.diag(np.square(risk_values))

    # Calculate the portfolio return
    portfolio_return = np.dot(weights, expected_returns)

    # Calculate the portfolio risk (standard deviation)
    portfolio_risk = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))

    return portfolio_return, portfolio_risk

def calculate_metrics(historical_data):
    log_ret=np.log(historical_data / historical_data.shift(1))
    annual_mu_df=log_ret.mean()*12
    sigma=log_ret.std()
    annual_std_df=sigma*np.sqrt(12)
    risk_list=[KeyValuePairDTO(index, value) for index, value in annual_std_df.items()]
    cagr_list=[KeyValuePairDTO(index, np.exp(value) - 1) for index, value in annual_mu_df.items()]
    return cagr_list,risk_list

def get_optimised_portfolio(portfolio):
    if not portfolio.is_metrics_enabled():
        portfolio = populate_portfolio_metrics(portfolio)
    optimal_equity_list,optimised_return,optimised_risk=optimize_portfolio(equity_data_list=portfolio.get_equities())
    portfolio.set_equities(optimal_equity_list)
    portfolio.set_optimised_return(optimised_return)
    portfolio.set_optimised_risk(optimised_risk)
    portfolio.is_optimised=True
    return portfolio

def optimize_portfolio(equity_data_list, risk_free_rate=0.03):
    # Step 2: Calculate expected returns
    expected_returns = [equity.get_cagr() for equity in equity_data_list]

    # Step 3: Calculate the covariance matrix (diagonal for independent equities)
    risk_values = [equity.get_risk() for equity in equity_data_list]
    cov_matrix = np.diag(np.square(risk_values))

    # Define the negative Sharpe ratio objective function
    def negative_sharpe(weights, expected_returns, cov_matrix, risk_free_rate):
        portfolio_return = np.sum(weights * expected_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev
        return -sharpe_ratio

    # Define constraints (e.g., sum of weights equals 1)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

    # Define bounds (weights between 0 and 1)
    bounds = tuple((0, 1) for asset in range(len(equity_data_list)))

    # Set initial guess for weights
    initial_weights = [1 / len(equity_data_list)] * len(equity_data_list)

    # Step 4: Solve the optimization problem
    result = minimize(negative_sharpe, initial_weights, args=(expected_returns, cov_matrix, risk_free_rate),
                      method='SLSQP', bounds=bounds, constraints=constraints)

    # Step 5: Extract the optimal weights
    optimal_weights = result.x
    for i, equity in enumerate(equity_data_list):
        equity.weight = optimal_weights[i]
    
    portfolio_return = np.sum(optimal_weights * expected_returns)

    # Step 7: Calculate the portfolio risk (standard deviation)
    portfolio_risk = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))

    # Return the optimal weights, return, and risk
    
    return equity_data_list,portfolio_return,portfolio_risk
