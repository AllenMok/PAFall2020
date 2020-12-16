
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.font_manager import FontProperties
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import random
import math


def polyfit(output,df,cityname,crashlag = 0,tablelag = 0,dpi=100):
    ''' by the Polynomial model from sklearn
        read in dataframe a city and training the model
        outout measurements and plot compare predicting reslut and real value
    '''
    if crashlag == 0 and tablelag == 0:
        print(cityname+' without lag')
        x = df[['table','crashes','trends']]
        y = df[['cases']]
        
    else:
        print(cityname+' with lag')
        lagcrashes= df.crashes[crashlag:].reset_index()
        lagtable = df.table[tablelag:].reset_index()
        trends = df.trends.reset_index()
        
        minlen = min(len(lagcrashes),len(lagtable),len(trends))
        
        x = pd.concat([lagcrashes[:minlen],lagtable[:minlen],trends[:minlen]],axis = 1)
        y = df[['cases']][:minlen]

    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)

    poly = PolynomialFeatures(degree=3)
    x = poly.fit_transform(x)
    
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.1,random_state=9999)
    # x_train = x_train.rolling(10).mean()
    # y_train = y_train.rolling(10).mean()

    
    regression = LinearRegression()
    regression.fit(x_train,y_train)
    y_predict_train = regression.predict(x_train)
    mse_train = np.sum((y_predict_train - y_train) ** 2) / len(y_train)
    rmse_train = math.sqrt(mse_train)
    print("R Square for training set: "+str(regression.score(x_train,y_train)))
    print(rmse_train)
    y_predict_test = regression.predict(x_test)
    mse_test = np.sum((y_predict_test - y_test) ** 2) / len(y_test)
    rmse_test = math.sqrt(mse_test)
    print("R Square for testting set: "+str(regression.score(x_test,y_test)))
    print(rmse_test)

    regression.fit(x,y)
    y_predict = regression.predict(x)
    mse_all = np.sum((y_predict - y) ** 2) / len(y)
    rmse_all = math.sqrt(mse_all)
    print("R Square for all data: "+str(regression.score(x,y)))
    print(rmse_all)
    
    # y_predict = pd.Series(y_predict.reshape(-1)).rolling(10).mean()
    y_predict = pd.Series(y_predict.reshape(-1))
    # y_train = y_train.rolling(10).mean()
    

    plt.figure(figsize=(15,4), dpi=dpi)
    plt.title('Polynomial Regression of Cases')
    plt.xlabel('Day')
    plt.ylabel('Case Number')
    plt.grid(True)
    l1, = plt.plot(range(len(y)),y.cases)
    l2, = plt.plot(range(len(y_predict)),y_predict,color = "red")
    plt.legend([l1,l2],['Origin Data','Prediction'],loc='lower left',frameon=False)
    if crashlag != 0 and tablelag != 0:
        title = cityname+' Prediction Line'+'with lag '+str(tablelag)+' days on OpenTable and lag '+str(crashlag)+' days on Traffic Accident'
        plt.title(title)
        plt.savefig(os.path.join(output,title+'.png'),format = 'png')
    else:
        title = cityname+' Prediction Line without lag'
        plt.title(title)
        plt.savefig(os.path.join(output,title+'.png'),format = 'png')
    
    return y_predict_test.reshape(-1)

def ttest(x,y):
    print(stats.levene(x,y))
    print(stats.ttest_ind(x,y,equal_var=False))
