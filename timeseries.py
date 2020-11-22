import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates as mdates

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