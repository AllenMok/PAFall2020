import numpy as np
import pandas as pd
import timeseries
import os

# global source  
# global origin  
source = 'timeseries'
origin = 'data'

def readCars2019():
    carFile = '_Car_TS.csv'
    try:
        NYC_Car_TS = pd.read_csv(os.path.join(source,'NYC_2019'+carFile),names=['date','cases'])
    except :
        print('FileNotExistError')

    try:
        LA_Car_TS = pd.read_csv(os.path.join(source,'LA_2019'+carFile),names=['date','cases'])
    except :
        print('FileNotExistError')

    try:
        FL_Car_TS = pd.read_csv(os.path.join(source,'FL_2019'+carFile),names=['date','cases'])
    except:
        print('FileNotExistError')

    return (NYC_Car_TS,LA_Car_TS,FL_Car_TS)

def readCars():
    # read in traffic accident cases data, if no time series data, generate time series data first
    carFile = '_Car_TS.csv'
    try:
        NYC_Car_TS = pd.read_csv(os.path.join(source,'NYC'+carFile),names=['date','cases'])
    except :
        timeseries.getTransTSFile('NYC_2020.csv','NYC'+carFile,'NYC')
        NYC_Car_TS = pd.read_csv(os.path.join(source,'NYC'+carFile),names=['date','cases'])

    try:
        LA_Car_TS = pd.read_csv(os.path.join(source,'LA'+carFile),names=['date','cases'])
    except :
        timeseries.getTransTSFile('LA_2020.csv','LA'+carFile,'LA')
        LA_Car_TS = pd.read_csv(os.path.join(source,'LA'+carFile),names=['date','cases'])

    try:
        FL_Car_TS = pd.read_csv(os.path.join(source,'FL'+carFile),names=['date','cases'])
    except:
        print('FileNotExistError')

    return (NYC_Car_TS,LA_Car_TS,FL_Car_TS)

def readCovid():
    # read in covid cases data, if no time series data, generate time series data first
    caseFile = '_Case_TS.csv'
    try:
        NYC_Case_TS = pd.read_csv(os.path.join(source,'NYC'+caseFile),names=['date','cases'])
        NYC_Case_TS = NYC_Case_TS.fillna(0)
    except :
        timeseries.getCaseTSFile_NYC('NYC','NYC'+caseFile,'NYC_COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv')
        NYC_Case_TS = pd.read_csv(os.path.join(source,'NYC'+caseFile),names=['date','cases'])
        NYC_Case_TS = NYC_Case_TS.fillna(0)
    try:
        LA_Case_TS = pd.read_csv(os.path.join(source,'LA'+caseFile),names=['date','cases'])
    except :
        timeseries.getCaseTSFile('LA','LA'+caseFile,'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
        LA_Case_TS = pd.read_csv(os.path.join(source,'LA'+caseFile),names=['date','cases'])

    try:
        FL_Case_TS = pd.read_csv(os.path.join(source,'FL'+caseFile),names=['date','cases'])
    except :
        timeseries.getCaseTSFile('FL','FL'+caseFile,'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')
        FL_Case_TS = pd.read_csv(os.path.join(source,'FL'+caseFile),names=['date','cases'])

    return NYC_Case_TS,LA_Case_TS,FL_Case_TS

def readTable():
    # read in opentable reservation rate data, if no time series data, generate time series data first
    otFile = "_Opentable_TS.csv" 
    try:
        NYC_Opentable_TS = pd.read_csv(os.path.join(source,'NYC'+otFile),names=['date','percnetage'])
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','city','New York','NYC'+otFile)
        NYC_Opentable_TS = pd.read_csv(os.path.join(source,'NYC'+otFile),names=['date','percnetage'])

    try:
        LA_Opentable_TS = pd.read_csv(os.path.join(source,'LA'+otFile),names=['date','percnetage'])   
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','city','Los Angeles','LA'+otFile)
        LA_Opentable_TS = pd.read_csv(os.path.join(source,'LA'+otFile),names=['date','percnetage'])
    
    try:
        FL_Opentable_TS = pd.read_csv(os.path.join(source,'FL'+otFile),names=['date','percnetage'])
    except:    
        timeseries.opentable('YoY_Seated_Diner_Data.csv','state','Florida','FL'+otFile)
        FL_Opentable_TS = pd.read_csv(os.path.join(source,'FL'+otFile),names=['date','percnetage'])
    return NYC_Opentable_TS,LA_Opentable_TS,FL_Opentable_TS

def readGoogleTrends():
    # read in google trends search data, if no time series data, generate time series data first
    gtFile = "_GoogleTrends.csv"
    NYC_GT = timeseries.googletrends(os.path.join(source,'NYC'+gtFile),'NYC',name = ['date','percnetage'])
    LA_GT = timeseries.googletrends(os.path.join(source,'LA'+gtFile),'LA',name = ['date','percnetage'])
    FL_GT = timeseries.googletrends(os.path.join(source,'FL'+gtFile),'FL',name = ['date','percnetage'])
    return NYC_GT,LA_GT,FL_GT




