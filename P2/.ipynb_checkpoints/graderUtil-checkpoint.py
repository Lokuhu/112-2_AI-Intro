import json
import os
import pandas as pd
from sklearn import metrics
#import sys

task_dir = "./task"
py_command = "python3"
py_code = "submission.py"

def accuracy_score(list_pred,list_test):
    #print(list_pred)
    #print(list_test)
    if len(list_pred) != len(list_test):
        print("The length of the prediction result is not correct!")
        return 0
    elif len([x for x in list_pred if x not in set(list_test)])>0: 
        print("The format of the prediction result is not correct!")
        return 0
    else:
        return metrics.accuracy_score(list_pred, list_test)*100
        
def load_file(filename):
    df = pd.DataFrame()
    file_in = os.path.join(task_dir,filename)
    if os.path.exists(file_in):
        df = pd.read_csv(file_in)
    else:
        print("No such file: " + file_in)
    return df

def load_testing_file(filename="test01.csv"):
    df = pd.DataFrame()
    file_in = os.path.join(task_dir,filename)
    if os.path.exists(file_in):
        df = pd.read_csv(file_in)
    else:
        print("No such file: " + file_in)
    return df 

def load_answer_file(filename="answer01.csv"):
    df = pd.DataFrame()
    file_in = os.path.join(task_dir,filename)
    if os.path.exists(file_in):
        df = pd.read_csv(file_in)
    else:
        print("No such file: " + file_in)
    return df
