import pandas as pd
import numpy as np
import math


# Helper functions
def time_pass(x):
    return x*math.exp(np.random.normal())


def predicted_value(x):
    return polynomial_coefficients[0]*x**2 + polynomial_coefficients[1]*x +polynomial_coefficients[2]


if __name__ == "__main__":

    # Option
    STRIKE_PRICE = 1.1
    MATURITY = 6

    # Model configuration
    SPOT = 1
    STEP_SIZE = 1
    STEPS = MATURITY // STEP_SIZE
    PATH_SZIE = 5
    RATE = 0.06
    DF = math.exp(-RATE)

    # Generate the initial state
    d = {'t0': [SPOT for _ in range(PATH_SZIE)]}
    data = pd.DataFrame(d)

    # Generate the simulated paths
    for i in range(STEPS):
        data['t{}'.format(i+1)] = data['t0']
        data.iloc[:, i+1] = data.iloc[:, i].apply(lambda x: time_pass(x))

    # Loop backward
    for i in reversed(range(2, STEPS+1)):
        current = data[['t{}'.format(i-1), 't{}'.format(i)]] # Get two consecutive cols
        ITM = current[current.iloc[:, 0] < STRIKE_PRICE]
        ITM.iloc[:, -1] = ITM.iloc[:, -1].apply(lambda x: max(STRIKE_PRICE-x, 0))

        # Regression
        polynomial_coefficients = np.polyfit(ITM.iloc[:,0], ITM.iloc[:,1]*DF, 2)
        print(polynomial_coefficients)

        # Calculate prediction value based on the regression results
        ITM['predicted_'+'t{}'.format(i-1)] = ITM.iloc[:,0].apply(predicted_value)