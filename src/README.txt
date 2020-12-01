PA Fall2020 Term Project

Time Series Analytics of Covid-19 Cases based on People Mobility Data 
@author: Yihan Mo, Yin Xu

This is a reference for setting up the PA Term Project (based on Python). In this project, we conduct time-series analysis based on Covid-19 Cases data from CDC and alternative data represent people mobility (OpenTable Reservation Rate and Traffic Accident cases). We determined the time lag between dependent variable and independent variables. And based on this conclusion, we compare the difference between models, determined the positive influence of time lag on the predictive model.

The project can be run directly by executing the main.py file

main.py:
main.py, the main class, control the work flow of the project. Read in files and transfer them into time series, clean and normalize time series, take Granger causality analysis and then build the predicting model.

readfile.py:
Class implement file reading. Read in raw data from CSV files, if the time series data exist, read in the time series data if it exist, else get generate time series data from the raw data. The time series data will have a CSV file as intermedia file.

timeseries.py:
Class generate time series data from the raw data, transfer the raw data into time series data.

plot.py:
Class implement plotting function, plot the the data into line chart. The output will be in '/plot_output'.

granger.py:
Class implement granger causality test for time series data, detect the significant of granger causality and time lag between variables.

predict.py:
Class implement polynomial regression, take the data and time lag, out put predict result and measurements.

/src:
Fold store all source code

/data:
Fold store the original raw data

/flowchart:
Fold store the flow chart that of our project

/timeseries:
Fold store the intermedia file for time series.

/plot_output:
Fold store the visualization result.

