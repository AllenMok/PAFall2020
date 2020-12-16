
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import grangercausalitytests 


def stationarytest(dataseries):
    # test data is stationary or not
    result = adfuller(dataseries, autolag='AIC') 
    print(f'ADF Statistic: {result[0]}') 
    print(f'p-value: {result[1]}')
    return result[1]

def difference(dataset, interval=1): 
    # preprocessing step to transform data into stationary
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval] 
        diff.append(value)
    return pd.Series(diff)