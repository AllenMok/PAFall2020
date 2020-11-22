
import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates
import granger
import plot
import timeseries
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.stattools import grangercausalitytests 

pd.set_option('display.max_columns', None)

sourcepath = "source"

def main():
    #date_day = pd.date_range(start='1/1/2020', end='9/30/2020')


    carFile = '_Car_TS.csv'
    try:
        NYC_Car_TS = pd.read_csv('NYC'+carFile,names=['date','cases'])
    except :
        timeseries.getTransTSFile('NYC_2020.csv','NYC'+carFile,'NYC')
        NYC_Car_TS = pd.read_csv('NYC'+carFile,names=['date','cases'])

    try:
        LA_Car_TS = pd.read_csv('LA'+carFile,names=['date','cases'])
    except :
        timeseries.getTransTSFile('LA_2020.csv','LA'+carFile,'LA')
        LA_Car_TS = pd.read_csv('LA'+carFile,names=['date','cases'])

    try:
        FL_Car_TS = pd.read_csv('FL'+carFile,names=['date','cases'])
    except:
        print('FileNotExistError')
    
    # print(FL_Car_TS)
    caseFile = '_Case_TS.csv'
    try:
        NYC_Case_TS = pd.read_csv('NYC'+caseFile,names=['date','cases'])
        NYC_Case_TS = NYC_Case_TS.fillna(0)
    except :
        timeseries.getCaseTSFile_NYC('NYC','NYC'+caseFile,'NYC_COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv')
        NYC_Case_TS = pd.read_csv('NYC'+caseFile,names=['date','cases'])
        NYC_Case_TS = NYC_Case_TS.fillna(0)
    try:
        LA_Case_TS = pd.read_csv('LA'+caseFile,names=['date','cases'])
    except :
        timeseries.getCaseTSFile('LA','LA'+caseFile,'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
        LA_Case_TS = pd.read_csv('LA'+caseFile,names=['date','cases'])

    try:
        FL_Case_TS = pd.read_csv('FL'+caseFile,names=['date','cases'])
    except :
        timeseries.getCaseTSFile('FL','FL'+caseFile,'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
        FL_Case_TS = pd.read_csv('FL'+caseFile,names=['date','cases'])
    
    otFile = "_Opentable_TS.csv"
    
    try:
        NYC_Opentable_TS = pd.read_csv('NYC'+otFile,names=['date','percnetage'])
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','city','New York','NYC'+otFile)
        NYC_Opentable_TS = pd.read_csv('NYC'+otFile,names=['date','percnetage'])

    try:
        LA_Opentable_TS = pd.read_csv('LA'+otFile,names=['date','percnetage'])   
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','city','Los Angeles','LA'+otFile)
        LA_Opentable_TS = pd.read_csv('LA'+otFile,names=['date','percnetage'])
    
    try:
        FL_Opentable_TS = pd.read_csv('FL'+otFile,names=['date','percnetage'])
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','state','Florida','FL'+otFile)
        FL_Opentable_TS = pd.read_csv('FL'+otFile,names=['date','percnetage'])

    # plot.plot_df(LA_Case_TS, x=LA_Case_TS['date'], y=LA_Case_TS['cases'].rolling(7).mean(), title='LA_COVID') #rolling 
    # plot.plot_df(NYC_Case_TS, x=NYC_Case_TS['date'], y=NYC_Case_TS['cases'].rolling(7).mean(), title='NYC_COVID')
    # plot.plot_df(NYC_Car_TS, x=NYC_Car_TS['date'], y=NYC_Car_TS['cases'].rolling(7).mean(), title='NYC_Car')
    # plot.plot_df(LA_Car_TS, x=LA_Car_TS['date'], y=LA_Car_TS['cases'].rolling(7).mean(), title='LA_Car')
    # plot.plot_df(x=NYC_Opentable_TS['date'], y=NYC_Opentable_TS['percnetage'].rolling(7).mean(), title='NYC_'+'Opentable_TS')
    # plot.plot_df(Opentable_LA_TS, x=Opentable_LA_TS['date'], y=Opentable_LA_TS['percnetage'].rolling(7).mean(), title='LA_'+'_OpentableTS')    
    
    # plot.plot_df_2var(x1=NYC_Car_TS['date'], y1=NYC_Car_TS['cases'].rolling(7).mean(),x2=NYC_Opentable_TS['date'], y2=NYC_Opentable_TS['percnetage'].rolling(7).mean(), title='NYC OpenTable VS Vehicle Crashes',y1label='Crash Cases',y2label='Percnetage',line1 = 'car crashes',line2 = 'opentable')
    # plot.plot_df_2var(x1=NYC_Case_TS['date'], y1=NYC_Case_TS['cases'].rolling(7).mean(),x2=NYC_Opentable_TS['date'], y2=NYC_Opentable_TS['percnetage'].rolling(7).mean(), title='NYC OpenTable VS COVID Cases',y1label='Covid Cases',y2label='Percnetage',line1 = 'covid case',line2 = 'opentable')
    # plot.plot_df_2var(x1=NYC_Case_TS['date'], y1=NYC_Case_TS['cases'].rolling(7).mean(),x2=NYC_Car_TS['date'], y2=NYC_Car_TS['cases'].rolling(7).mean(), title='NYC Car Crashes VS COIVD Cases',y1label='Covid Cases',y2label='Crash Cases',line1 = 'covid case',line2 = 'car crashes')
    
    # plot.plot_df_2var(x1=LA_Car_TS['date'], y1=LA_Car_TS['cases'].rolling(7).mean(),x2=LA_Opentable_TS['date'], y2=LA_Opentable_TS['percnetage'].rolling(7).mean(), title='LA OpenTable VS Vehicle Crashes',y1label='Crash Cases',y2label='Percnetage',line1 = 'car crashes',line2 = 'opentable')
    # plot.plot_df_2var(x1=LA_Case_TS['date'], y1=LA_Case_TS['cases'].rolling(7).mean(),x2=LA_Opentable_TS['date'], y2=LA_Opentable_TS['percnetage'].rolling(7).mean(), title='LA OpenTable VS COVID Cases',y1label='Covid Cases',y2label='Percnetage',line1 = 'covid case',line2 = 'opentable')
    # plot.plot_df_2var(x1=LA_Case_TS['date'], y1=LA_Case_TS['cases'].rolling(7).mean(),x2=LA_Car_TS['date'], y2=LA_Car_TS['cases'].rolling(7).mean(), title='LA Car Crashes VS COIVD Cases',y1label='Covid Cases',y2label='Crash Cases',line1 = 'covid case',line2 = 'car crashes')
       
    # plot.plot_df_2var(x1=FL_Car_TS['date'], y1=FL_Car_TS['cases'].rolling(7).mean(),x2=FL_Opentable_TS['date'], y2=FL_Opentable_TS['percnetage'].rolling(7).mean(), title='FL OpenTable VS Vehicle Crashes',y1label='Crash Cases',y2label='Percnetage',line1 = 'car crashes',line2 = 'opentable')
    # plot.plot_df_2var(x1=FL_Case_TS['date'], y1=FL_Case_TS['cases'].rolling(7).mean(),x2=FL_Opentable_TS['date'], y2=FL_Opentable_TS['percnetage'].rolling(7).mean(), title='FL OpenTable VS COVID Cases',y1label='Covid Cases',y2label='Percnetage',line1 = 'covid case',line2 = 'opentable')
    # plot.plot_df_2var(x1=FL_Case_TS['date'], y1=FL_Case_TS['cases'].rolling(7).mean(),x2=FL_Car_TS['date'], y2=FL_Car_TS['cases'].rolling(7).mean(), title='FL Car Crashes VS COVID Cases',y1label='Covid Cases',y2label='Crash Cases',line1 = 'covid case',line2 = 'car crashes')

    # granger.stationarytest(LA_Case_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(LA_Car_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(LA_Opentable_TS['percnetage'].rolling(10).mean().fillna(0))
    # grangerCase(LA_Case_TS,LA_Car_TS,var1st = False,var2st = True)
    # grangerCase(LA_Case_TS,LA_Opentable_TS,var1st = False,var2st = True)
   
    
    # granger.stationarytest(FL_Case_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(FL_Car_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(FL_Opentable_TS['percnetage'].rolling(10).mean().fillna(0))
    # grangerCase(FL_Case_TS,FL_Car_TS,var1st = True,var2st = True)
    # grangerCase(FL_Case_TS,FL_Opentable_TS,var1st = True,var2st = False)
   
    
    # granger.stationarytest(NYC_Case_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(NYC_Car_TS['cases'].rolling(10).mean().fillna(0))
    # granger.stationarytest(NYC_Opentable_TS['percnetage'].rolling(10).mean().fillna(0))
    # grangerCase(NYC_Case_TS,NYC_Car_TS,var1st = False,var2st = True)
    # grangerCase(NYC_Case_TS,NYC_Opentable_TS,var1st = False,var2st = True)
    

    # st_FL_Car = granger.difference(FL_Car_TS['cases'])
    # st_FL_Opentable = granger.difference(FL_Opentable_TS['percnetage'])
    # new_df = pd.concat([st_FL_Car,st_FL_Opentable],axis = 1)
    # grangercausalitytests(new_df[[0,1]],maxlag = 20)

    # st_LA_Car = granger.difference(LA_Car_TS['cases'])
    # st_LA_Opentable = granger.difference(LA_Opentable_TS['percnetage'])
    # new_df = pd.concat([st_LA_Car,st_LA_Opentable],axis = 1)
    # grangercausalitytests(new_df[[0,1]],maxlag = 20)

    st_NYC_Car = granger.difference(NYC_Car_TS['cases'])
    st_NYC_Opentable = granger.difference(NYC_Opentable_TS['percnetage'])
    new_df = pd.concat([st_NYC_Car,st_NYC_Opentable],axis = 1)
    grangercausalitytests(new_df[[0,1]],maxlag = 20)

def grangerCase(var1,var2,var1st = False,var2st = False,window = 10,lag = 40):
    if var1st == True:
        st_var1 = pd.Series(var1.iloc[:,1].rolling(window).mean().fillna(0))
    else:
        st_var1 = pd.Series(granger.difference(var1.iloc[:,1].rolling(window).mean().fillna(0)))
    if var2st == True:
        st_var2 = pd.Series(var2.iloc[:,1].rolling(window).mean().fillna(0))
    else:
        st_var2 = pd.Series(granger.difference(var2.iloc[:,1].rolling(window).mean().fillna(0)))
    new_df = pd.concat([st_var1,st_var2],axis = 1).fillna(0)
    new_df.columns = [0,1]
    new_df.drop(new_df.tail(1).index,inplace=True)
    print(new_df)
    grangercausalitytests(new_df[[0,1]],maxlag = lag)











    # if var1st == True:
    #     st_var1 = pd.Series(var1.iloc[:,1].rolling(window).mean().fillna(0))
    # else:
    #     st_var1 = pd.Series(np.diff(var1.iloc[:,1].rolling(window).mean().fillna(0)))
    # if var2st == True:
    #     st_var2 = pd.Series(var2.iloc[:,1].rolling(window).mean().fillna(0))
    # else:
    #     st_var2 = pd.Series(np.diff(var2.iloc[:,1].rolling(window).mean().fillna(0)))
    # new_df = pd.concat([st_var1,st_var2],axis = 1).fillna(0)
    # new_df.columns = [0,1]
    # new_df.drop(new_df.tail(1).index,inplace=True)
    # print(new_df)
    # grangercausalitytests(new_df[[0,1]],maxlag = lag)

if __name__ == '__main__':
    main()


