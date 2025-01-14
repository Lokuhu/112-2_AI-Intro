import json
import numpy as np
import os
import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
import sys
import graderUtil
import seaborn as sns
#######################################################################
# Do not make any change in this block
# a dict stores the final result
task_result = {
    "y_pred": []
} 

# read task file content
training_filename = sys.argv[1]
testing_filename = sys.argv[2]
answer_filename = sys.argv[3]

df = graderUtil.load_file(training_filename)
X_test = graderUtil.load_testing_file(testing_filename)
y_test = graderUtil.load_answer_file(answer_filename)

#print(df.sample(5))
#print(X_test.sample(5))
#print(y_test)
#
##########################################################
# BEGIN_YOUR_CODE

# terminal use
# cd .\112-2\二234_人工智慧概論\P2
# python submission.py disease_60.csv test01.csv answer01.csv

rs=2

df = df.astype(int) #轉成boolean

# training dataset
a = df.iloc[:,[0,2,4,13,15,16]] #17 kinds of data
#print(df.columns[0:16])
b = df.iloc[:,-1]

# print(a.columns)
# print(a_test.columns)

# normalization: min-max normalization
scaler = MinMaxScaler(feature_range=(0, 1)).fit(a) 
#print(scaler.data_min_)
#print(scaler.data_max_)
a_scaled = scaler.transform(a) 
#print(X_scaled)
#print('(scaled) max: ', X_scaled.max(axis=0))
#print('(scaled) min: ', X_scaled.min(axis=0))


#這行修改到老師設置的參數了！ 
a_train, a_test, b_train, b_test = train_test_split(a_scaled,b, test_size=0.2, random_state=rs)

# initialization
model = Perceptron()
# optimization
model.fit(a_train, b_train)

#檢查用 print(X.columns)
#檢查用 print(X_test.columns)

# training: performance
b_pred_train = model.predict(a_train)
print("the training result:",np.round(metrics.accuracy_score(b_pred_train, b_train),5))

# testing: performance
b_pred_test = model.predict(a_test)
print("the testing result",np.round(metrics.accuracy_score(b_pred_test, b_test),5))


X_test = X_test.astype(int) #x is disease y is ans
X_test01 = X_test.iloc[:,[0,2,4,13,15,16]]
# answer = y_test.iloc[:,0]
# min-max
# test01scaler = MinMaxScaler(feature_range=(0, 1)).fit(X_test01)
# Z score
test01scaler = MinMaxScaler().fit(X_test01)
test01_scaled = test01scaler.transform(X_test01)
y_pred_test = model.predict(test01_scaled)

# Predict using the trained model on the provided test set
task_result["y_pred"] = list(y_pred_test)

#檢查用 print(df.columns)


# END_YOUR_CODE
# Do Not Make Any Change BELOW
#######################################################################

# output your final result
print("Prediction:")
print(task_result["y_pred"])
print("Score(80%): " + str(graderUtil.accuracy_score(task_result['y_pred'],y_test['Target'])))