import numpy as np
from numpy.core.numeric import tensordot
import pandas as pd
import pickle
import matplotlib.pyplot as matplot
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor as MLP
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix

def accuracy(pred_labels,true_labels):
        lengte = len(true_labels)
        all_errors = 0
        for pred_label,true_label in zip(pred_labels,true_labels):
            if pred_label < 0.5:
                pred_label = 0
            else:
                pred_label = 1
            if pred_label == true_label:
                all_errors += 1
            

        MAE = all_errors / lengte
        return MAE

def plt(true_labels,pred_labels,label,length,yrange,ax):
    if ax == None:
        fig, ax = matplot.subplots()
    index = np.arange(length)
    bar_width = 0.25
    opacity = 0.8

    rects1 = ax.bar(index, true_labels[:length], bar_width, alpha=opacity,color='r',label='True_labels')
    rects2 = ax.bar(index + bar_width, pred_labels[:length], bar_width,alpha=opacity,color='b',label='Pred_labels')
    rects2 = ax.bar(index + 2*bar_width, abs(true_labels[:length]-pred_labels[:length]), bar_width,alpha=opacity,color='g',label='Absolute Error')
    ax.ticklabel_format(style='plain')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(label)
    if yrange != None:
        ax.set_ylim(yrange)
    ax.legend()

    if ax == None:
        matplot.show()

class MLPRegressor:
    def __init__(self,dataset,input_data,label,test_size=0.2,random_state=42):
        self.label = label
        dataset = pd.read_csv(dataset)
        input_data = dataset[input_data]
        input_data = (input_data - input_data.mean()) / (input_data.max() - input_data.min()) # stap 3
        label = dataset[self.label]

        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(input_data,label,test_size=test_size,random_state=random_state)

    def plot(self,length,yrange=None,ax=None):
        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test

        plt(true_labels,pred_labels,self.label,length,yrange,ax)

    def train(self,hidden_layer_sizes):
        self.model = MLP(hidden_layer_sizes)
        self.model.fit(self.data_train,self.labels_train)
        
        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test

        acc = accuracy(pred_labels,true_labels)
        print('Het model heeft een nauwkeurigheid van {}.'.format(acc))

    def epochtrain(self,hidden_layer_sizes,epochs,num_data):
        self.model = MLP(hidden_layer_sizes,max_iter=1,warm_start=True)

        train_accs = []
        test_accs = []

        for epoch in range(epochs):
            self.model.fit(self.data_train[:num_data], self.labels_test[:num_data])

            pred_labels = self.model.predict(self.data_train[:num_data])
            true_labels = self.labels_train[:num_data]
            train_acc = accuracy(pred_labels,true_labels)
            train_accs.append(train_acc)

            pred_labels = self.model.predict(self.data_test[:1000])
            true_labels = self.labels_test[:1000]
            test_acc = accuracy(pred_labels,true_labels)
            test_accs.append(test_acc)

        matplot.plot(train_accs,label='Train acc')
        matplot.plot(test_accs,label='Test acc')
        matplot.xlabel('Epoch')
        matplot.ylabel('Accuracy')
        matplot.ylim(0.1)
        matplot.legend()
        matplot.plot()