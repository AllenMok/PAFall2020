
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates

pd.set_option('display.max_columns', None)


def main():
    date_day = pd.date_range(start='1/1/2020', end='9/30/2020')
    # try:
    #     LA_Car_TS = pd.read_csv('LA_TS.csv',names=["date","cases"])
    #     NYC_Car_TS = pd.read_csv('NYC_TS.csv',names=["date","cases"])
    # except :
    #     getTransTSFile()

    # try:
    #     NYC_Case_TS = pd.read_csv('NYC_Case_TS.csv',names=["date","cases"])
    # except :
    #     getCaseTSFile_NYC('NYC','NYC_Case_TS.csv','source/NYC_COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv')
    #     NYC_Case_TS = pd.read_csv('NYC_Case_TS.csv',names=["date","cases"])
    
    # try:
    #     LA_Case_TS = pd.read_csv('LA_Case_TS.csv',names=["date","cases"])
    # except :
    #     getCaseTSFile('LA','LA_Case_TS.csv')
    #     LA_Case_TS = pd.read_csv('LA_Case_TS.csv',names=["date","cases"])

    # plot_df(LA_Case_TS, x=LA_Case_TS['date'], y=LA_Case_TS['cases'].rolling(7).mean(), title='LA_COVID') #rolling 
    # plot_df(NYC_Case_TS, x=NYC_Case_TS['date'], y=NYC_Case_TS['cases'].rolling(7).mean(), title='NYC_COVID')
    # plot_df(NYC_Case_TS, x=NYC_Case_TS['date'], y=NYC_Case_TS['cases'], title='NYC_COVID')
    # plot_df(LA_Case_TS, x=LA_Case_TS['date'], y=LA_Case_TS['cases'], title='LA_COVID')


    # plot_df(NYC_Car_TS, x=NYC_Car_TS['date'], y=NYC_Car_TS['cases'].rolling(7).mean(), title='NYC_Car')
    # plot_df(LA_Car_TS, x=LA_Car_TS['date'], y=LA_Car_TS['cases'].rolling(7).mean(), title='LA_Car')
    
    try:
        Opentable_TS = pd.read_csv("Opentable_"+"NYC"+"_TS.csv",names=["date","percnetage"])

    except:    
        opentable("source/YoY_Seated_Diner_Data.csv","city","New York","Opentable_"+"NYC"+"_TS.csv")
        Opentable_TS = pd.read_csv("Opentable_"+"NYC"+"_TS.csv",names=["date","percnetage"])

    plot_df(Opentable_TS, x=Opentable_TS['date'], y=Opentable_TS['percnetage'].rolling(7).mean(), title="Opentable_"+"NYC"+"_TS")
    
    try:
        Opentable_TS = pd.read_csv("Opentable_"+"LA"+"_TS.csv",names=["date","percnetage"])
        
    except:    
        opentable("source/YoY_Seated_Diner_Data.csv","city","Los Angeles","Opentable_"+"LA"+"_TS.csv")
        Opentable_TS = pd.read_csv("Opentable_"+"LA"+"_TS.csv",names=["date","percnetage"])
    
    plot_df(Opentable_TS, x=Opentable_TS['date'], y=Opentable_TS['percnetage'].rolling(7).mean(), title="Opentable_"+"LA"+"_TS")
    
def plot_df(df, x, y, title="", xlabel='Cases', ylabel='Time', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(x, y, color='red') 
    ax= plt.gca()
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gcf().autofmt_xdate() #
    plt.savefig(title+'.png',format = 'png')
    plt.show()

def getCaseTSFile_NYC(location,filename,sourcename,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    case_data = pd.read_csv(sourcename)
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
    
def getCaseTSFile(location,filename,date_day = pd.date_range(start='2/20/2020', end='9/30/2020')):
    case_data = pd.read_csv('source/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
    case_data = case_data[['submission_date','state','new_case']]
    case_data = case_data[case_data['state'].str.contains(location)]

    case_data['submission_date'] = pd.to_datetime(case_data['submission_date'],format = '%m/%d/%Y')
    
    
    Case_toTS = pd.Series(0,index=date_day)

    for i, v in Case_toTS.items():

        # case_data[case_data['submission_date']==i]
        daycase = case_data[case_data['submission_date']==i]["new_case"]
        if daycase.size == 0:
            Case_toTS[i] = 0
        else:
            Case_toTS[i] = daycase.values[0]
    Case_toTS.to_csv(filename, encoding='utf-8', index=True,header=False)


def getTransTSFile():
    LA_data = pd.read_csv('source/LA_2020.csv')
    NYC_data = pd.read_csv('source/NYC_2020.csv')
    
    LA_data = LA_data[['Date Occurred','Time Occurred']]
    NYC_data = NYC_data[['CRASH DATE','CRASH TIME']]

    NYC_data['CRASH TIME'] = NYC_data['CRASH TIME'].str.replace(':','')
    NYC_data['CRASH DATE'] = pd.to_datetime(NYC_data['CRASH DATE'],format='%m/%d/%y')
    LA_data['Date Occurred'] = pd.to_datetime(LA_data['Date Occurred'],format='%m/%d/%y')

    LA_toTS = toTS(LA_data['Date Occurred'])
    NYC_toTS = toTS(NYC_data['CRASH DATE'])

    LA_toTS.to_csv('LA_TS.csv', encoding='utf-8', index=True,header=False)
    NYC_toTS.to_csv('NYC_TS.csv', encoding='utf-8', index=True,header=False)


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
    optable = pd.read_csv(source)
    optable = optable[optable['Type'].str.contains(type)]
    optable = optable[optable['Name'].str.contains(location)]
    optable = optable.T[2:]
    optable.columns = ["Percnetage"]
    optable.index = pd.date_range(start='2/18/2020', end='10/21/2020')

    Case_toTS = pd.Series(0,index=date_day,dtype="float64")

    for i, v in Case_toTS.items():
        if i in optable.index:
            Case_toTS[i] = round(100+optable["Percnetage"][i],2)
        else:
            Case_toTS[i] = np.NaN

    Case_toTS.to_csv(filename, encoding='utf-8', index=True,header=False)

if __name__ == '__main__':
    main()


