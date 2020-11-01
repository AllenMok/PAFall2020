
import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates

pd.set_option('display.max_columns', None)

sourcepath = "source"

def main():
    #date_day = pd.date_range(start='1/1/2020', end='9/30/2020')

    
    carFile = '_Car_TS.csv'
    try:
        NYC_Car_TS = pd.read_csv('NYC'+carFile,names=['date','cases'])
    except :
        getTransTSFile('NYC_2020.csv','NYC'+carFile,'NYC')
        NYC_Car_TS = pd.read_csv('NYC'+carFile,names=['date','cases'])

    try:
        LA_Car_TS = pd.read_csv('LA'+carFile,names=['date','cases'])
    except :
        getTransTSFile('LA_2020.csv','LA'+carFile,'LA')
        LA_Car_TS = pd.read_csv('LA'+carFile,names=['date','cases'])

    caseFile = '_Case_TS.csv'
    try:
        NYC_Case_TS = pd.read_csv('NYC'+caseFile,names=['date','cases'])
    except :
        getCaseTSFile_NYC('NYC','NYC'+caseFile,'NYC_COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv')
        NYC_Case_TS = pd.read_csv('NYC'+caseFile,names=['date','cases'])
    
    try:
        LA_Case_TS = pd.read_csv('LA'+caseFile,names=['date','cases'])
    except :
        getCaseTSFile('LA','LA'+caseFile,'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
        LA_Case_TS = pd.read_csv('LA'+caseFile,names=['date','cases'])
    
    otFile = "_Opentable_TS.csv"
    try:
        Opentable_NYC_TS = pd.read_csv('NYC'+otFile,names=['date','percnetage'])

    except:    
        opentable('YoY_Seated_Diner_Data.csv','city','New York','NYC'+otFile)
        Opentable_NYC_TS = pd.read_csv('NYC'+otFile,names=['date','percnetage'])

    try:
        Opentable_LA_TS = pd.read_csv('LA'+otFile,names=['date','percnetage'])
        
    except:    
        opentable('YoY_Seated_Diner_Data.csv','city','Los Angeles','LA'+otFile)
        Opentable_LA_TS = pd.read_csv('LA'+otFile,names=['date','percnetage'])
    
    plot_df(LA_Case_TS, x=LA_Case_TS['date'], y=LA_Case_TS['cases'].rolling(7).mean(), title='LA_COVID') #rolling 
    plot_df(NYC_Case_TS, x=NYC_Case_TS['date'], y=NYC_Case_TS['cases'].rolling(7).mean(), title='NYC_COVID')
    plot_df(NYC_Car_TS, x=NYC_Car_TS['date'], y=NYC_Car_TS['cases'].rolling(7).mean(), title='NYC_Car')
    plot_df(LA_Car_TS, x=LA_Car_TS['date'], y=LA_Car_TS['cases'].rolling(7).mean(), title='LA_Car')
    plot_df(Opentable_NYC_TS, x=Opentable_NYC_TS['date'], y=Opentable_NYC_TS['percnetage'].rolling(7).mean(), title='NYC_'+'Opentable_TS')
    plot_df(Opentable_LA_TS, x=Opentable_LA_TS['date'], y=Opentable_LA_TS['percnetage'].rolling(7).mean(), title='LA_'+'_OpentableTS')
    
    
def plot_df(df, x, y, title='', xlabel='Cases', ylabel='Time', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(x, y, color='red') 
    ax= plt.gca()
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate() #
    plt.savefig(title+'.png',format = 'png')
    # plt.show()

def getCaseTSFile_NYC(location,filename,source,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    case_data = pd.read_csv(os.path.join(sourcepath,source))
    case_data = case_data[['DATE_OF_INTEREST','CASE_COUNT']]
    case_data['DATE_OF_INTEREST'] = pd.to_datetime(case_data['DATE_OF_INTEREST'],format = '%m/%d/%Y')
    
    
    Case_toTS = pd.Series(0,index=date_day)

    for i, v in Case_toTS.items():

        # case_data[case_data['submission_date']==i]
        daycase = case_data[case_data['DATE_OF_INTEREST']==i]['CASE_COUNT']
        if daycase.size == 0:
            Case_toTS[i] = np.NaN
        else:
            Case_toTS[i] = daycase.values[0]
    Case_toTS.to_csv(filename, encoding='utf-8', index=True,header=False)
    
def getCaseTSFile(location,filename,source,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    case_data = pd.read_csv(os.path.join(sourcepath,source))
    case_data = case_data[['submission_date','state','new_case']]
    case_data = case_data[case_data['state'].str.contains(location)]

    case_data['submission_date'] = pd.to_datetime(case_data['submission_date'],format = '%m/%d/%Y')
    
    
    Case_toTS = pd.Series(0,index=date_day)

    for i, v in Case_toTS.items():

        daycase = case_data[case_data['submission_date']==i]['new_case']
        if daycase.size == 0:
            Case_toTS[i] = 0
        else:
            Case_toTS[i] = daycase.values[0]
    Case_toTS.to_csv(filename, encoding='utf-8', index=True,header=False)


def getTransTSFile(source,outputname,city):
    data = pd.read_csv(os.path.join(sourcepath,source))
    
    if city == 'LA':
        data = data[['Date Occurred']]
        data['Date Occurred'] = pd.to_datetime(data['Date Occurred'],format='%m/%d/%y')
        data = toTS(data['Date Occurred'])

    elif city == 'NYC':
        data = data[['CRASH DATE']]
        data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'],format='%m/%d/%y')
        data = toTS(data['CRASH DATE'])
    
    data.to_csv(outputname, encoding='utf-8', index=True,header=False)
    


def toTS(records,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    crashes = []
    for i in date_day:
        count = 0
        for j in records:
            if i == j:
                count+=1
        crashes.append(count)
    return pd.Series(crashes,index=date_day)

def opentable(source,type,location,filename,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    optable = pd.read_csv(os.path.join(sourcepath,source))
    optable = optable[optable['Type'].str.contains(type)]
    optable = optable[optable['Name'].str.contains(location)]
    optable = optable.T[2:]
    optable.columns = ['Percnetage']
    optable.index = pd.date_range(start='2/18/2020', end='10/21/2020')

    Case_toTS = pd.Series(0,index=date_day,dtype='float64')

    for i, v in Case_toTS.items():
        if i in optable.index:
            Case_toTS[i] = round(100+optable['Percnetage'][i],2)
        else:
            Case_toTS[i] = np.NaN

    Case_toTS.to_csv(filename, encoding='utf-8', index=True,header=False)

if __name__ == '__main__':
    main()


