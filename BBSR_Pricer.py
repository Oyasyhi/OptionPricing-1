import numpy as np
import scipy.stats as sps
import math
import option

def BSM(S: float, K: float,q: float, r: float, sigma: float, T: float, option_type: str) -> float:
    d1 = (np.log(S/K) + (r + 0.5 * sigma ** 2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == "Call":
        return S * np.exp(-q * T) * sps.norm.cdf(d1) - K * np.exp(-r * T) * sps.norm.cdf(d2)
    elif option_type == "Put":
        return K * np.exp(-r * T) * sps.norm.cdf(-d2) - S * np.exp(-q * T) * sps.norm.cdf(-d1)
    else:
        return -1.0

def BBS(steps: int,S: float, K: float, r: float, sigma: float, T: float, option_type: str) -> float:
    dt = T/steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1/u
    p = (np.exp(r * dt) - d)/(u - d)
    q = 1-p
    temps = 0
    # stock_price[no_ups, no_downs]
    stock_price = np.zeros((steps + 1, steps + 1))
    stock_price[0,0] = S
    for diag in range(1,steps + 1):
        stock_price[0,diag] = stock_price[0, diag-1] * d
        for j in range(1, diag + 1):
            stock_price[j,diag - j] = stock_price[j - 1,diag - j] * u
    # option_val[no_ups, no_downs]
    option_val = np.zeros((steps + 1, steps + 1))
    # option payoff at time T
    if option_type == "Call":
        for i in range(steps + 1):
            option_val[i, steps - i] = max(stock_price[i, steps - i] - K, 0)
        # option payoff at time t(N-1)
        for i in range(steps):
            temps = stock_price[i, steps - 1 - i]
            # Values differ from sample code because I use this line in the notes, while they use BSM without the max
            option_val[i, steps - 1 - i] = max(BSM(temps, K, 0, r, sigma, dt, "Call"), temps - K, 0)
    elif option_type == "Put":
        for i in range(steps + 1):
            option_val[i, steps - i] = max(K - stock_price[i, steps - i], 0)
        # option payoff at time t(N-1)
        for i in range(steps):
            temps = stock_price[i, steps - 1 - i]
            option_val[i, steps - 1 - i] = max(BSM(temps, K, 0, r, sigma, dt, "Put"), K - temps, 0)
    # over here the steps - 1 and steps diagonal have been filled
    # only need to fill diagonals from [0,steps - 1] inclusive
    if option_type == "Call":
        for diag in range(steps - 2, -1, -1):
            for j in range(diag + 1):
                option_val[j, diag - j] = max(np.exp(-r * dt) * (p * option_val[j + 1, diag - j] + q * option_val[j, diag - j + 1]),
                                              stock_price[j, diag - j] - K,
                                              0)
    elif option_type == "Put":
        for diag in range(steps - 2, -1, -1):
            for j in range(diag + 1):
                option_val[j, diag - j] = max(np.exp(-r * dt) * (p * option_val[j + 1, diag - j] + q * option_val[j, diag - j + 1]), K - stock_price[j, diag - j], 0)

    return option_val[0,0]

def BBSR(steps: int, S: float, K: float, r: float, sigma: float, T: float, option_type)-> float:
    return 2 * BBS(2 * steps, S, K, r, sigma, T, option_type) - BBS(steps, S, K, r, sigma, T, option_type)


class BBSRPricer:
    def __init__(self, steps_size: float, spot: float, rate: float, vol: float):
        self.steps_size = steps_size
        self.spot = spot
        self.rate = rate
        self.vol = vol

    def __call__(self, opt: option.AmericanPutOption):
        steps = math.ceil(opt.ttm//self.steps_size)
        return BBSR(steps, self.spot, opt.strike, self.rate, self.vol, opt.ttm, "Put")
