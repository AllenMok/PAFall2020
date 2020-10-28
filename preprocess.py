import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

LA_data = pd.read_csv('LA_2020.csv')
NYC_data = pd.read_csv('NYC_2020.csv')

cvd = pd.read_csv('United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')

LA_data = LA_data[['Date Occurred','Time Occurred']]
NYC_data = NYC_data[['CRASH DATE','CRASH TIME']]

NYC_data['CRASH TIME'] = NYC_data['CRASH TIME'].str.replace(':','')

NYC_data['CRASH DATE'] = pd.to_datetime(NYC_data['CRASH DATE'],format='%m/%d/%y')
LA_data['Date Occurred'] = pd.to_datetime(LA_data['Date Occurred'],format='%m/%d/%y')

LA_toTS = toTS(LA_data['Date Occurred'])

def toTS(records):
    date_day = pd.date_range(start='1/1/2020', end='9/30/2020')
    date_week = pd.date_range(start='1/1/2020', periods=40, freq='W')
    for 
