import numpy as np
import pandas as pd
import time
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates

from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import grangercausalitytests 

import granger
import plot
import timeseries
import readfile
import predict

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



def main():
   
    os.chdir('../')
    out = 'plot_output'
    cars = readfile.readCars('timeseries')
    case = readfile.readCovid('timeseries')
    table = readfile.readTable('timeseries')
    ny = pd.DataFrame({'NYC':cars[0].iloc[:,0],'crashes':cars[0].iloc[:,1],'cases':case[0].iloc[:,1],'table':table[0].iloc[:,1]})
    la = pd.DataFrame({'LA':cars[1].iloc[:,0],'crashes':cars[1].iloc[:,1],'cases':case[1].iloc[:,1],'table':table[1].iloc[:,1]})
    fl = pd.DataFrame({'FL':cars[2].iloc[:,0],'crashes':cars[2].iloc[:,1],'cases':case[2].iloc[:,1],'table':table[2].iloc[:,1]})
    dfs = [ny,la,fl]
    interpolate(dfs)
    trends = readfile.readGoogleTrends('timeseries')
    ny['trends'] = trends[0].values
    la['trends'] = trends[1].values
    fl['trends'] = trends[2].values
    # baseplots(out,dfs)

    # grangertest(la)
    # plot.replotTable(out,fl,lag = 21)
    # plot.replotTable(out,la,lag = 21)
    # plot.replotTable(out,ny,lag = 21)
    # plot.replotCrash(out,fl,16)
    # plot.replotCrash(out,la,16)
    # plot.replotCrash(out,ny,16)

    # ny_nolag = predict.polyfit(out,ny,'NY')
    # ny_lag = predict.polyfit(out,ny,'NY',crashlag = 16,tablelag = 21)
    # predict.ttest(ny_lag,ny_nolag)

    # la_nolag = predict.polyfit(out,la,'LA')
    # la_lag = predict.polyfit(out,la,'LA',crashlag = 16,tablelag = 21)
    # predict.ttest(la_lag,la_nolag)

    
    fl_nolag = predict.polyfit(out,fl,'FL')
    fl_lag = predict.polyfit(out,fl,'FL',crashlag = 16,tablelag = 21)
    predict.ttest(fl_lag,fl_nolag)
    

def baseplots(output,dfs,interval = 10):
    for df in dfs:
        plot.plot_df_2var(output,x1=df.index, y1=df.crashes.rolling(interval).mean(),x2=df.index, y2=df.table.rolling(interval).mean(), title= df.columns[0]+' OpenTable & Vehicle Crashes',y1label='Crash Cases',y2label='Percnetage',line1 = 'car crashes',line2 = 'opentable')
        plot.plot_df_2var(output,x1=df.index, y1=df.cases.rolling(interval).mean(),x2=df.index, y2=df.table.rolling(interval).mean(), title=df.columns[0]+' OpenTable & COVID Cases',y1label='Covid Cases',y2label='Percnetage',line1 = 'covid case',line2 = 'opentable')
        plot.plot_df_2var(output,x1=df.index, y1=df.cases.rolling(interval).mean(),x2=df.index, y2=df.crashes.rolling(interval).mean(), title=df.columns[0]+' Car Crashes & COIVD Cases',y1label='Covid Cases',y2label='Crash Cases',line1 = 'covid case',line2 = 'car crashes')
        plot.plot_df_2var(output,x1=df.index, y1=df.cases.rolling(interval).mean(),x2=df.index, y2=df.trends.rolling(interval).mean(), title=df.columns[0]+' Google Trends & COIVD Cases',y1label='Covid Cases',y2label='Google Trends',line1 = 'covid case',line2 = 'trends')

def grangertest(df):
    case_pval = granger.stationarytest(df.cases)
    crash_pval = granger.stationarytest(df.crashes)
    table_pval = granger.stationarytest(df.table)
    # grangerCase(df.table,df.crashes,var1st = (table_pval<0.05),var2st = (crash_pval<0.05),lag = 15,cut = [25,-1]) # car gc open
    grangerCase(df.cases,df.table,var1st = (case_pval<0.05),var2st = (table_pval<0.05),lag = 40,cut = [25,-1]) # open gc case
    # grangerCase(df.cases,df.crashes,var1st = (case_pval<0.05),var2st = (crash_pval<0.05),lag = 40,cut = [25,-1]) # crash gc cas

def interpolate(dfs):
    for df in dfs:
        df.cases = df.cases.replace(0,np.nan)
        df.loc[df.cases < 0,'cases'] = np.nan
        df.cases = df.cases.interpolate(method='linear', axis=0).fillna(0)

def grangerCase(var1,var2,var1st = False,var2st = False,window = 10,lag = 40,cut = [20,-1]):
    if var1st == True:
        st_var1 = pd.Series(var1.rolling(window).mean().fillna(0))
    else:
        st_var1 = pd.Series(granger.difference(var1.rolling(window).mean()))
    if var2st == True:
        st_var2 = pd.Series(var2.rolling(window).mean().fillna(0))
    else:
        st_var2 = pd.Series(granger.difference(var2.rolling(window).mean()))
    
    df = pd.concat([st_var1,st_var2],axis = 1).fillna(0)
    df.columns = [0,1]
    df.drop(df.tail(1).index,inplace=True)
    df = df[cut[0]:cut[1]]
    df_norm = (df - df.min()) / (df.max() - df.min())  
    result = grangercausalitytests(df[[0,1]],maxlag = lag)
    return df_norm
    
if __name__ == '__main__':
    main()