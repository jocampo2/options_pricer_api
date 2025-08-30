import numpy as np
from scipy.stats import norm

def black_scholes_call(spot, strike, maturity, interest_rate, volatility):

    d1 = (np.log(spot / strike) + (interest_rate + 0.5 * volatility**2) * maturity) / (volatility * np.sqrt(maturity))
    d2 = d1 - volatility * np.sqrt(maturity)

    return spot * norm.cdf(d1) - strike * np.exp(-interest_rate * maturity) * norm.cdf(d2)