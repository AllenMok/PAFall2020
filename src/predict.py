
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.font_manager import FontProperties
from sklearn.preprocessing import MinMaxScaler

def polyfit(output,df,cityname):
    y_train = df[['cases']]
    x_train = df[['table','crashes','trends']]

    x_train = x_train.rolling(10).mean()[10:]
    y_train = y_train.rolling(10).mean()[10:]
    
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)

    poly = PolynomialFeatures(degree=3)
    x_train = poly.fit_transform(x_train)
    # poly.fit(x_train,y_train)
    
    regression = LinearRegression()
    regression.fit(x_train,y_train)
    y_predict = regression.predict(x_train)
    print(regression.score(x_train,y_train))
    
    y_predict = pd.Series(y_predict.reshape(-1)).rolling(10).mean()
    plt.figure()
    plt.title('Polynomial Regression of Cases')
    plt.xlabel('Day')
    plt.ylabel('Case Number')
    plt.grid(True)
    l1, = plt.plot(range(len(y_train)),y_train.cases)
    l2, = plt.plot(range(len(y_predict)),y_predict,color = "red")
    plt.legend([l1,l2],['Origin Data','Prediction'],loc='lower left',frameon=False)
    plt.savefig(os.path.join(output,cityname+' Prediction Line.png'),format = 'png')
    # plt.show()
