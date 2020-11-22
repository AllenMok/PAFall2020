
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import grangercausalitytests 


def plot_df(df, x, y, title="", xlabel='Year', ylabel='Inflation Rate', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(x, y, color='tab:red') 
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel) 
    plt.show()

def stationarytest(dataseries):
    result = adfuller(dataseries, autolag='AIC') 
    print(f'ADF Statistic: {result[0]}') 
    print(f'p-value: {result[1]}')

def difference(dataset, interval=1): 
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval] 
        diff.append(value)
    return pd.Series(diff)