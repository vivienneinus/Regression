# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:45:28 2018

@author: vwzheng
"""

import os
import numpy as np
import pandas as pd
from math import *
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

dtype_dict = {'bathrooms':float, 'waterfront':int, 'sqft_above':int, 
              'sqft_living15':float, 'grade':int, 'yr_renovated':int, 
              'price':float, 'bedrooms':float, 'zipcode':str, 'long':float, 
              'sqft_lot15':float, 'sqft_living':float, 'floors':float, 
              'condition':int, 'lat':float, 'date':str, 'sqft_basement':int, 
              'yr_built':int, 'id':str, 'sqft_lot':int, 'view':int}

add=(
'D:/Downloads/vivienne/ML/Regression_UW/Wk6_NearestNeighbor&KernelRegression'
)
os.chdir(add)
train = pd.read_csv('kc_house_data_small_train.csv', dtype=dtype_dict)
test = pd.read_csv('kc_house_data_small_test.csv', dtype=dtype_dict)
valid = pd.read_csv('kc_house_data_validation.csv', dtype=dtype_dict)

#Take a data set, a list of features to be used as inputs, 
#and a name of the output
def get_numpy_data(data, features, output):
    #add a constant column to a data_Frame if it doesn't have
    data['constant'] = 1 
    #prepend variable 'constant' to the features list
    if 'constant' not in features:
        features.insert(0, 'constant')
    #select the columns of data_Frame given by the ‘features’ list 
    feature_matrix = data[features].values
    #assign the column of data associated with the target to the ‘output’
    output_array = data[output].values
    return (feature_matrix, output_array)

#Normalize columns of a given feature matrix
def normalize_features(feature_matrix):
    #Compute 2-norms of columns
    norms = np.linalg.norm(feature_matrix, axis=0) 
    #Normalize columns and perform element-wise division
    normalized_features = feature_matrix/norms
    return (normalized_features, norms)

feature_list = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
                'waterfront', 'view', 'condition', 'grade', 'sqft_above',  
                'sqft_basement', 'yr_built', 'yr_renovated', 'lat', 'long',  
                'sqft_living15', 'sqft_lot15']

features_train, output_train = get_numpy_data(train, feature_list, 'price')
features_test, output_test = get_numpy_data(test, feature_list, 'price')
features_valid, output_valid = get_numpy_data(valid, feature_list, 'price')
#Normalize features to compute distances
#Divide each column of the training feature matrix by its 2-norm, 
#so that the transformed column has unit norm    
features_train, norms = normalize_features(features_train) 
#Store the norms of the features in the train set for test and valid sets
features_test = features_test / norms
features_valid = features_valid / norms

#The query house to be the first house of the test set
print (features_test[0])
print (features_train[9])

#Euclidean distance
euclidean_distance = np.sqrt(((features_train[9] - features_test[0])**2
                              ).sum())
print (euclidean_distance)

#Loop to compute the Euclidean distance from the query house to each of 
#the first 10 houses in the training set
dist_dict = {}
for i in range(0,10):
    dist_dict[i] = np.sqrt(np.sum((features_train[i] - features_test[0])**2))
    print (i, np.sqrt(np.sum((features_train[i] - features_test[0])**2)))

#Among the first 10 training houses, 
#which house is the closest to the query house    
print (min(dist_dict.items(), key=lambda x: x[1]))

#Compute the element-wise difference between the features of the query house 
#(features_test[0]) and the first 3 training houses (features_train[0:3])
for i in range(3):
    print (features_train[i]-features_test[0])
    # should print 3 vectors of length 18

print (features_train[0:3] - features_test[0])

#Verify that vectorization works
results = features_train[0:3] - features_test[0]
print (results[0] - (features_train[0]-features_test[0]))
#Should print all 0's if results[0] == (features_train[0]-features_test[0])
print (results[1] - (features_train[1]-features_test[0]))
#Should print all 0's if results[1] == (features_train[1]-features_test[0])
print (results[2] - (features_train[2]-features_test[0]))
#Should print all 0's if results[2] == (features_train[2]-features_test[0])    

#Nearest neighbor regression
#element-wise difference between the features of the query house and 
#the i-th training house
diff = features_train - features_test[0]
print (diff[-1].sum())  #should be -0.0934339605842
#Compute the sum across each row --> axis = 1; column --> axis = 0
np.sum(diff**2, axis = 1)
print (np.sum(diff**2, axis=1)[15]) #the 16th sum of squares across each row
print (np.sum(diff[15]**2)) #the sum of squares for the 16th row
#Compute the Euclidean distances from the query to all the instances
distances = np.sqrt(np.sum(diff**2, axis = 1))
print(distances[100]) #should contain 0.0237082324496

#Write a function that computes the distances from a query house to 
#all training houses
#Perform 1-nearest neighbor regression
def compute_distances(features_instance, features_query):
    diff = features_instance - features_query
    distances = np.sqrt(np.sum(diff**2,axis=1))
    return distances

#Take the query house to be third house of the test set (features_test[2])   
third_house_distances = compute_distances(features_train, features_test[2])
#Return the indices of the training houses closest to the query house
#print(third_house_distances.argsort()[:1])    
index_test3 = third_house_distances.argsort()[0] #382
print(third_house_distances.min()) #0.00286049555751
print(third_house_distances[index_test3]) #should be the same above
pred_val = output_train[index_test3] #predicted value based on 1-NN reg

#Perform k-nearest neighbor regression
def k_nearest_neighbors(k, features_instance, features_query):
    distances = compute_distances(features_instance, features_query) 
    #return 1-col matrix
    neighbors = np.argsort(distances, axis=0)[:k] #indices of the houses 
    return neighbors

#Return the indices of the 4 training houses closest to the query house
indices = k_nearest_neighbors(4, features_train, features_test[2])
#[ 382 1149 4087 3142]
print(third_house_distances.argsort()[:4]) #should be the same above

#Write a function that predicts the value of a given query house. 
#Take the average of the prices of the k nearest neighbors in the train set
#The function should return a predicted value of the query house 
def predict_output_of_query(k, features_instance, output, features_query):
    neighbors = k_nearest_neighbors(k, features_instance, features_query)
    prediction = np.mean(output[neighbors])
    return prediction

#Predict the value of the query house using k-nearest neighbors with k=4 
prediction = predict_output_of_query(4, features_train, output_train,
                                     features_test[2])

#Write a function to predict the value of each and every house in a query set
def predict_output(k, features_instance, output_instance, 
                   features_query_matrix):
    predictions = []
    nrow = features_query_matrix.shape[0]
    for i in range(nrow):
        avg = predict_output_of_query(k, features_instance, output_instance,
                                      features_query_matrix[i])
        predictions.append(avg)
    return predictions   
 
#Predict the first 10 houses in the test set, using k=10. 
predictions = predict_output(10, features_train, output_train, 
                             features_test[0:10]) #return a list
#Index of the house in this query set that has the lowest predicted value
index_test10 = np.array(predictions).argsort()[0]   
min_value = min(predictions) #the predicted value of this house
test10_index = predictions.index(min_value) #should return the same index


#Choose the best value of k using a validation set
list_RSS = []
for k in range(1,16):
    predictions = predict_output(k, features_train, output_train,
                                 features_valid)
    RSS = sum((predictions - output_valid)**2)
    list_RSS.append(RSS)
k_opt = list_RSS.index(min(list_RSS)) + 1    
    
plt.plot(range(1,16), list_RSS,'bo-')

#Compute the RSS on the TEST data using the value of k
predictions_test = predict_output(k_opt, features_train, output_train, 
                                  features_test)
RSS_test = sum((predictions_test - output_test)**2)
