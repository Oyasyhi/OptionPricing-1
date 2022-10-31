import pandas as pd

from LSMC_Pricer import LSMCPricer
from BBSR_Pricer import BBSRPricer
from option import AmericanPutOption
import numpy as np

if __name__ == "__main__":
    def grid(step_size, rate, vol):
        LSMC_pricer = LSMCPricer(spot=1, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=1, steps_size=step_size, rate=rate, vol=vol)

        res = {}
        for i in np.arange(0.6, 2.1, step=0.05):  # strike
            for j in range(1, 6):  # ttm
                strike = i
                ttm = j
                opt = AmericanPutOption(strike, ttm)
                LSMC_res = LSMC_pricer(opt)
                BBSR_res = BBSR_pricer(opt)
                res.update({f'{strike},{ttm}': [LSMC_res, BBSR_res]})
                print(i, j)

        return res
# S, K ,sigma, T

    def ttm_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        res = pd.DataFrame(columns = ["ttm", "LSMC", "BBSR"])
        size = ttm / 100
        for i in np.arange(ttm, ttm - size, step = -size):
            opt = AmericanPutOption(strike, i)
            # opt.ttm = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            # print(i)
        return res
    def strike_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        opt = AmericanPutOption(strike, ttm)
        res = pd.DataFrame(columns = ["Strike", "LSMC", "BBSR"])
        n = 10
        size = strike / n
        for i in np.arange(strike - n / 2 * size, strike  + n/2 * size, step = size):
            opt.strike = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            print(i)
        return res
    def spot2_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        opt = AmericanPutOption(strike, ttm)
        res = pd.DataFrame(columns = ["Spot", "LSMC", "BBSR"])
        n = 100
        size = ttm / n
        for i in np.arange(ttm, 0 - size, step = size):
            opt.ttm = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            print(i)
        return res

    # result = grid(0.1, 0.06, 0.2)
    def spot_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        opt = AmericanPutOption(strike, ttm)
        res = pd.DataFrame(columns = ["Spot", "LSMC", "BBSR"])
        n = 100
        size = spot / n
        for i in np.arange(spot - n/2 * size, spot + (n/2 + 1) * size , step = size):
            LSMC_pricer.spot = i
            BBSR_pricer.spot = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            print(i)
        return res

    def vol_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        res = pd.DataFrame(columns = ["Vol", "LSMC", "BBSR"])
        opt = AmericanPutOption(strike, ttm)
        n = 100
        size = vol / n
        for i in np.arange(vol - n /2 * size, vol + (n /2 + 1) * size , step = size):
            BBSR_pricer.vol = i
            LSMC_pricer.vol = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            print(i)
        return res


    def rate_test(step_size, rate, vol, spot, strike, ttm):
        LSMC_pricer = LSMCPricer(spot=spot, step_size=step_size, rate=rate, vol=vol, path_size=10000)
        BBSR_pricer = BBSRPricer(spot=spot, steps_size=step_size, rate=rate, vol=vol)
        res = pd.DataFrame(columns = ["Rate", "LSMC", "BBSR"])
        opt = AmericanPutOption(strike, ttm)
        n = 10
        size = rate / n
        for i in np.arange(rate - n * size, rate + (n + 1) * size , step = size):
            BBSR_pricer.rate = i
            LSMC_pricer.rate = i
            LSMC_res = LSMC_pricer(opt)
            BBSR_res = BBSR_pricer(opt)
            res.loc[len(res.index)] = [i, LSMC_res, BBSR_res]
            print(i)
        return res
    result = strike_test(0.1, 0.03, 0.6, 100, 100, 2.0)
    print(result)

