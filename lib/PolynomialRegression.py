#!python

# Initial settings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from math import sqrt


class RegressionByDegree:
    def __init__(self, p_degree = 1):
        self.__degree = p_degree
        self.__poly_regressor = None
        self.__regressor = None
        self.__transformed_column = None
        self.__data_train = None
        self.__data_train_y = None
        #print("RegressionByDegree with degree ", self.__degree, " called.")
    
    def __del__(self):
        print("Destructor called.")

    def apply_regression(self):
        self.__poly_regressor = PolynomialFeatures(degree = self.__degree)
        self.__transformed_column = self.__poly_regressor.fit_transform(self.__data_train)
        self.__regressor = LinearRegression()
        self.__regressor.fit(self.__transformed_column, self.__data_train_y)
        self.__predict_y = self.__regressor.predict(self.__poly_regressor.fit_transform(self.__data_train))
       
    def plot_data(self, p_xlabel, p_ylabel, p_title):
        plt.scatter(self.__data_train, self.__data_train_y, color = 'red')
        plt.ylabel(p_ylabel)
        plt.xlabel(p_xlabel)
        plt.title(p_title)
    
    def plot_prediction(self, p_xlabel, p_ylabel, p_title):
        plt.plot(self.__data_train, self.__predict_y, color = 'blue')
        plt.ylabel(p_ylabel)
        plt.xlabel(p_xlabel)
        plt.title(p_title)
        plt.legend([self.__degree])   
        plt.show()
    
    def set_data_train(self, p_data_train):
        self.__data_train = p_data_train

    def set_data_train_y(self, p_data_train_y):
        self.__data_train_y = p_data_train_y
     
    def get_data_train(self):
        return self.__data_train
    
    def get_data_train_y(self):
        return self.__data_train_y
    
    def get_X_transformed_column(self):
        return self.__transformed_column
    
    def get_regressor(self):
        return self.__regressor       
    
    def get_degree(self):
        return self.__degree    
    
    def set_predict_y(self, p_data):
        self.__predict_y = self.__regressor.predict(self.__poly_regressor.fit_transform(p_data))
    
    def get_predict_y(self):
        return self.__predict_y
        
    def set_model_evaluation(self, p_data, p_data_y):
        self.set_predict_y(p_data)
        self.__RMSE = np.sqrt(mean_squared_error(p_data_y, self.__predict_y))
        self.__MSE = mean_squared_error(p_data_y, self.__predict_y)
        self.__MAE = mean_absolute_error(p_data_y, self.__predict_y)
        self.__r2 = r2_score(p_data_y, self.__predict_y)
        self.__adj_r2 = 1 - (1 - self.__r2) * (len(p_data) - 1) / (len(p_data) - (p_data.shape[1]) - 1)
        self.__MAPE = np.mean( np.abs( (p_data_y - self.__predict_y) / p_data_y ) )*100

    def get_model_evaluation_info(self):
        print(' RMSE =        ', format(self.__RMSE, '.2'), '\n',
              'MSE =         ', format(self.__MSE, '.2f'), '\n',
              'MAE =         ', format(self.__MAE, '.2f'), '\n',
              'R2 =          ', format(self.__r2, '.2f'), '\n',
              'Adjusted R2 = ', format(self.__adj_r2, '.2f'), '\n',
              'MAPE =        ', format(self.__MAPE[0], '.2f'))

    def get_adj_r2(self):
        return format(self.__adj_r2, '.2f')

    def get_r2(self):
        return format(self.__r2, '.2f')

    def get_MSE(self):
        return format(self.__MSE, '.2f')

    def get_MAE(self):
        return format(self.__MAE, '.2f')

    def get_RMSE(self):
        return format(self.__RMSE, '.2f')

    def get_MAPE(self):
        return format(self.__MAPE[0], '.2f')

