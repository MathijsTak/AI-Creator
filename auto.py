import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
count = 1
MAE_list = []

dataset = pd.read_csv('C:/Users/Mathi/OneDrive - Corderius College/2021-2022/PWS/Cardiovascular Disease dataset/cardio_train.csv')

def MLPRegressor_model(hidden_layer_sizes,input_data_train,labels_train):
    model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes)
    print('training...')
    model.fit(input_data_train,labels_train)
    return model

def bereken_MAE(pred_labels,true_labels):
    all_errors = []
    for pred_label,true_label in zip(pred_labels,true_labels):

        absolute_error = abs(pred_label - true_label)

        all_errors.append(absolute_error)

        
    MAE = sum(all_errors) / len(all_errors)
    return MAE

while count <= 1000:
    input_data = dataset[['age','height','weight','gender','ap_hi','ap_lo','cholesterol','gluc','smoke','alco','active']]
    input_data = (input_data - input_data.mean()) / (input_data.max() - input_data.min())
    labels = dataset['cardio']
    input_data_train, input_data_test, labels_train, labels_test = train_test_split(input_data,labels,test_size=0.2,random_state=42)

    model = MLPRegressor_model([10,10,10],input_data_train,labels_train)
    pred_labels = model.predict(input_data_test)
    true_labels = labels_test

    MAE = bereken_MAE(pred_labels,true_labels)
    print('Het netwerk zit er gemiddeld {} naast.'.format(MAE))
    MAE_list.append(MAE)
    pkl_filename = str(count) + '.pkl'
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)
    count += 1

smallest = min(MAE_list)
print(1 + MAE_list.index(smallest))
    