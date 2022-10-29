from LSMC_Pricer import LSMCPricer
from BBSR_Pricer import BBSRPricer
from option import AmericanPutOption
import statistics

if __name__ == "__main__":
    option = AmericanPutOption(strike=1, ttm=1)
    LSMC_pricer = LSMCPricer(spot=1, step_size=0.01, rate=0.06, vol=0.2, path_size=10000)
    BBSR_pricer = BBSRPricer(spot=1, steps_size=0.01, rate=0.06, vol=0.2)

    repeat_time = 10
    LSMC_res = [LSMC_pricer(option) for _ in range(repeat_time)]
    BBSR_res = [BBSR_pricer(option) for _ in range(repeat_time)]
    diff_res = [LSMC_res[i]-BBSR_res[i] for i in range(repeat_time)]
    diff_percent_res = [diff_res[i]/BBSR_res[i] for i in range(repeat_time)]
    print(diff_res, statistics.mean(diff_percent_res), statistics.mean(diff_res), statistics.variance(diff_res))


