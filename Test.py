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

    result = grid(0.1, 0.06, 0.2)
    for key in result.keys():
        print(key, result[key][0], result[key][1], result[key][0] - result[key][1], (result[key][0] - result[key][1])/result[key][1])

