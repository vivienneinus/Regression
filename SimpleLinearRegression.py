# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 11:30:23 2019

@author: vwzheng
"""

import pandas as pd
import statsmodels.api as sm

#requires a dictionary of types for importing csv files
train_data = pd.read_csv('kc_house_train_data.csv', 
                         dtype = {'bathrooms':float, 'waterfront':int, 
                                  'sqft_above':int, 'sqft_living15':float, 
                                  'grade':int, 'yr_renovated':int, 
                                  'price':float, 'bedrooms':float, 
                                  'zipcode':str, 'long':float, 
                                  'sqft_lot15':float, 'sqft_living':float, 
                                  'floors':str, 'condition':int, 'lat':float, 
                                  'date':str, 'sqft_basement':int, 
                                  'yr_built':int, 'id':str, 'sqft_lot':int, 
                                  'view':int})
data.head()
lm = linear_model.LinearRegression()

#intercept and slope for simple linear regression
def simple_linear_regression(input_feature, output):
    model = sm.OLS(output, sm.add_constant(input_feature)).fit()
    return(model.params)

#predicted response variable for simple linear regression
def get_regression_predictions(input_feature, intercept, slope):
    predicted_output = []
    for data in input_feature:
        prediction = intercept + slope * data
        predicted_output.append(prediction)
    return(predicted_output)

#Residual Sum of Squares 
def get_residual_sum_of_squares(input_feature, output, intercept, slope):
    RS = []
    for i in range(len(input_feature)):
        RS.append((intercept + slope * input_feature[i] - output[i])**2)
    return(sum(RS))

#estimated_imput for simple liear regression
def inverse_regression_predictions(output, intercept, slope):
    estimated_input = []
    for i in range(len(output)):
        estimated_input.append((output[i] - intercept)/slope)
    return(estimated_input)

#----------response variable and predictive variable(s)----------
output = train_data['price']
input_feature = train_data['sqft_living']
intercept, slope = simple_linear_regression(input_feature, output)
RSS_slr = get_residual_sum_of_squares(input_feature, output, intercept, slope)
bedrooms = train_data['bedrooms']
coef1, coef2 = simple_linear_regression(bedrooms, output)
RSS_bedrooms = get_residual_sum_of_squares(bedrooms, output, coef1, coef2)