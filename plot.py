import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates


def plot_df_2var(x1, y1, x2, y2, title='', xlabel='Time', y1label='Cases',y2label='Cases',line1 = 'line1',line2 = 'line2', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    ax1= plt.gca()
    ax2= ax1.twinx()
    l1, = ax1.plot(x1, y1, color='red') 
    l2, = ax2.plot(x2, y2, color='blue') 
    
    ax1.set(title=title, xlabel=xlabel, ylabel=y1label)
    ax2.set(title=title, xlabel=xlabel, ylabel=y2label)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate() #
    plt.legend([l1,l2],[line1,line2],loc='best',frameon=False)
    
    
    plt.savefig(title+'.png',format = 'png')
    
    # plt.show()

def plot_df(x, y, title='', xlabel='Time', ylabel='Cases', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(x, y, color='red') 
    ax= plt.gca()
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate() #
    plt.savefig(title+'.png',format = 'png')
    # plt.show()

