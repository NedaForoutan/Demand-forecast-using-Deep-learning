# -*- coding: utf-8 -*-
"""retail

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TpIRst7XNcux6AWtp8KSLT5fIzoGwm4A
"""

import torch
import torch.nn as nn

import seaborn as sn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime
import math
# Importing the most popular regression libraries.
from sklearn.linear_model import LinearRegression 
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from xgboost import XGBRegressor

# import os
# print(os.listdir("../input"))
#pd.read_csv("../input/sales data-set.csv")

#loading data
feature = pd.read_csv('datasets_2296_3883_Features data set.csv')
store = pd.read_csv('datasets_2296_3883_stores data-set.csv')
sales = pd.read_csv('sales data-set.csv')

#merge all files in one data frame
data = sales.merge(feature, how = 'left', on=['Store', 'Date', 'IsHoliday'])
data = data.merge(store,how= "left", on=['Store'])
#print(len(data.columns))
#print(data.shape)

num_store = store.Type.value_counts()
print(num_store) # A has highest number of stores

holiday = data.IsHoliday.value_counts()
print(holiday)

#preprocessing
data=data.fillna(0)
#data.isna().sum()  #check for any NaN

print((data.Weekly_Sales<0).any())  #negative value in weekly sales
#ignore negative ones
data = data[data.Weekly_Sales>0]
print((data.Weekly_Sales<0).any())
print(data.shape)

#is there ant duplicate row
print(data.duplicated().sum())

#IsHoliday 0,1
data.IsHoliday = data.IsHoliday.replace({True: 1, False: 0})

#Type 1,2,3
data.Type = data.Type.replace({"A": 1, "B": 2, "C": 3})

print(data[:5])

#Normalizing
#def normalize():
scalar = MinMaxScaler(feature_range=(-1, 1))
norm_columns = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']
for col in norm_columns:
  data[col] = scalar.fit_transform(np.array(data[col]).reshape(-1,1))

data[:5]

#correlation matrix
cor_matrix = data.corr()
cor_matrix

#As we see MarkDown 4 and MarkDown1 are high correlated
f, ax = plt.subplots(figsize=(12, 9))
sn.heatmap(cor_matrix, vmax=.8, square=True, annot=True)
#plt.show()

data = data.sort_values(by='Date', ascending=True)

#splitting the data into train, validation, test
y = data['Weekly_Sales']
x = data.drop(['Weekly_Sales'], axis = 1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3) 
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.3)

#weighted holidays
def WMSE (X, Y, pred):
  weight = x.IsHoliday.apply(lambda holiday:5 if holiday else 1)
  return np.sum(weight * np.square(Y - pred), axis = 0) / np.sum(weight)

pd.to_datetime(data['Date'])[:5]

feature selction
window
CNN, CNN_LSTM