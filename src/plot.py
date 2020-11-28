import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates


def plot_df_2var(output,x1, y1, x2, y2, title='', xlabel='Time', y1label='Cases',y2label='Cases',line1 = 'line1',line2 = 'line2', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi) #figsize=(15,4), dpi=dpi
    ax1= plt.gca()
    ax2= ax1.twinx()
    l1, = ax1.plot(x1, y1, color='red') 
    l2, = ax2.plot(x2, y2, color='blue') 
    
    ax1.set(title=title, xlabel=xlabel, ylabel=y1label)
    ax2.set(title=title, xlabel=xlabel, ylabel=y2label)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate() #
    plt.legend([l1,l2],[line1,line2],loc='upper left',frameon=False)
    plt.grid(True)
    plt.savefig(os.path.join(output,title+'.png'),format = 'png')
    
    # plt.show()

def plot_df(output,x, y, title='', xlabel='Time', ylabel='Cases', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi) #figsize=(15,4), dpi=dpi
    plt.plot(x, y, color='red') 
    ax= plt.gca()
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.savefig(os.path.join(output,title+'.png'),format = 'png')
    # plt.show()

def replotTable(out,df,lag = 31):
    df = df[40:]
    case = df.cases[lag:]
    case.index = range(len(case))
    table = df.table
    table.index = range(len(table))
    plot_df_2var(out,x1=table.index[:150], y1=table.values[:150],x2=case.index[:150], y2=case.values[:150], title=df.columns[0]+' '+str(lag)+' days time lag adjusted OpenTable & COVID Cases',y1label='Table Reservation',y2label='Covid Cases',line1 = 'reservation',line2 = 'covid case')

def replotCrash(out,df,lag = 31):
    df = df[40:]
    case = df.cases[lag:]
    case.index = range(len(case))
    crash = df.crashes
    crash.index = range(len(crash))
    plot_df_2var(out,x1=crash.index[:150], y1=crash.values[:150],x2=case.index[:150], y2=case.values[:150], title=df.columns[0]+' '+str(lag)+' days time lag adjusted Vehicle Crashes & COVID Cases',y1label='Crashes Cases',y2label='Covid Cases',line1 = 'crash case',line2 = 'covid case')

def replotTrend(out,df,lag = 31):
    df = df[40:]
    case = df.cases[lag:]
    case.index = range(len(case))
    trends = df.trends
    trends.index = range(len(trends))
    plot_df_2var(out,x1=trends.index[:150], y1=trends.values[:150],x2=case.index[:150], y2=case.values[:150], title=df.columns[0]+' '+str(lag)+' days time lag adjusted Google Trends & COVID Cases',y1label='Google Trends',y2label='Covid Cases',line1 = 'trends',line2 = 'covid case')





