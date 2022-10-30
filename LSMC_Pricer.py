import pandas as pd
import numpy as np
import math


class LSMCPricer:
    def __init__(self, spot, step_size=1.0, path_size=1000, rate=0.06, vol=0.2):
        self.spot = spot
        self.step_size = step_size
        self.path_size = path_size
        self.rate = rate
        self.vol = vol

    def __call__(self, opt):
        steps = int(opt.ttm/self.step_size)
        df = math.exp(-self.rate*self.step_size)
        if (opt.ttm - self.step_size*steps) != 0:
            steps += 1
            last_time_period = opt.ttm - self.step_size*steps
            df_last = math.exp(-self.rate*last_time_period)
        else:
            last_time_period = self.step_size
            df_last = df

        def time_pass(x, dt):
            next = x * math.exp((self.rate - self.vol ** 2 / 2) * dt + self.vol * np.random.normal(0, math.sqrt(dt)))
            return next

        def option_exercise(spot):
            return max(opt.strike - spot, 0)

        def predicted_value(x, *coef):
            return x * (coef[0] * x + coef[1]) + coef[2]

        d = {'t0': [self.spot for _ in range(self.path_size)]}
        data = pd.DataFrame(d)

        for i in range(1, steps+1):
            time = self.step_size if not (i == steps) else last_time_period
            data['t{}'.format(i)] = data['t{}'.format(i-1)].apply(lambda x: time_pass(x, time))

        value = pd.DataFrame()
        value = pd.DataFrame.reindex_like(value, data)
        value.iloc[:, steps] = data.iloc[:, steps].apply(option_exercise)

        for i in reversed(range(2, steps + 1)):
            disc_fact = df if i != steps else df_last
            value['t{}'.format(i-1)] = value['t{}'.format(i)].apply(lambda x: x * disc_fact)

            current = pd.concat([data['t{}'.format(i - 1)], value['t{}'.format(i)]], axis=1)  # Get two consecutive cols
            ITM = current[current[f't{i-1}'] < opt.strike].copy()
            if len(ITM.iloc[:, 0]) != 0:  # If there is no ITM, we will not do exercise decision.
                # print("There are {} ITM trades".format(len(ITM.iloc[:, 0])))

                # Regression
                polynomial_coefficients = np.polyfit(ITM.iloc[:, 0], ITM.iloc[:, 1] * disc_fact, 2)

                # Calculate prediction value based on the regression results
                ITM['predicted_' + 't{}'.format(i - 1)] = ITM[f't{i-1}'].apply(predicted_value, args=tuple(polynomial_coefficients))
                ITM[f'exercise_return_t{i - 1}'] = ITM.iloc[:, 0].apply(option_exercise)
                ITM['exercise'] = ITM[f'predicted_t{i - 1}'] < ITM[f'exercise_return_t{i - 1}']
                value.iloc[list(ITM[ITM['exercise'] == True].index), i - 1] = ITM[ITM['exercise'] == True][
                    f'exercise_return_t{i - 1}']
            else:
                pass

        price = value.iloc[:, 1].apply(lambda x: x * df).mean()
        return price
