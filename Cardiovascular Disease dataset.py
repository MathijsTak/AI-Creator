import numpy as np
from numpy.core.numeric import tensordot
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import csv
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix

# 1. Het csv bestand van de dataset definiëren
# 2. De kolommen die gebruikt worden als input data definiëren
# 3. Input data omzetten in waardes van -1 tot 1
# 4. De label van je dataset definiëren
# 5. De data verdelen in training data en test data

dataset = pd.read_csv('dataset.csv') # dataset.csv veranderen in de naam van het csv bestand vb. data.csv
input_data = dataset[['column', 'column']] # column veranderen naar de naam van de kolom vb. age
input_data = (input_data - input_data.mean()) / (input_data.max() - input_data.min()) # stap 3
label = dataset['label'] # label vervangen voor de label van de dataset vb. death

input_data_train, input_data_test, labels_train, labels_test = train_test_split(input_data,label,test_size=0.2,random_state=42) # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

pkl_filename = input('Name of model: ') # Om het model op te slaan voert de gebruiker de naam van het model in

def bereken_MAE(pred_labels,true_labels):
    all_errors = []
    for pred_label,true_label in zip(pred_labels,true_labels):
        if pred_label < 0.5:
            pred_label = 0
        else:
            pred_label = 1

        absolute_error = abs(pred_label - true_label)

        all_errors.append(absolute_error)

        
    MAE = sum(all_errors) / len(all_errors)
    return MAE

def bereken_accuracy(pred_labels,true_labels):
    lengte = len(true_labels) # op deze manier werkt de code foutloos
    all_errors = 0
    for pred_label,true_label in zip(pred_labels,true_labels):
        if pred_label < 0.5:
            pred_label = 0
        else:
            pred_label = 1
        if pred_label == true_label:
            all_errors += 1
        

    acc = all_errors / lengte
    return acc

def dplot(true_labels,pred_labels,dlen,yrange = None,ax=None):
    if ax == None:
        fig, ax = plt.subplots()
    index = np.arange(dlen)
    bar_width = 0.25
    opacity = 0.8

    rects1 = ax.bar(index, true_labels[:dlen], bar_width, alpha=opacity,color='r',label='True_labels')
    rects2 = ax.bar(index + bar_width, pred_labels[:dlen], bar_width,alpha=opacity,color='b',label='Pred_labels')
    rects2 = ax.bar(index + 2*bar_width, abs(true_labels[:dlen]-pred_labels[:dlen]), bar_width,alpha=opacity,color='g',label='Absolute Error')
    ax.ticklabel_format(style='plain')
    ax.set_xlabel('Patient')
    ax.set_ylabel('')
    ax.set_title('Cardio')
    if yrange != None:
        ax.set_ylim(yrange)
    ax.legend()

    if ax == None:
        plt.show()

def epoch(hidden_layer_sizes,epochs,training):
    train_accs = []
    test_accs = []


    nums_data= [50,100,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000]
    for num_data in nums_data:
        hidden_layer_sizes = hidden_layer_sizes
        epochs = int(epochs)

        if training == 1:
            model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,
                                max_iter=epochs,  #run maar 1 epoch per keer dat we network.fit aanroepen
                                warm_start=True #ga verder met de gewichten van het netwerk uit de vorige network.fit (Als dit False was, werden de gewichten elke epoch weggegooit)
                                )
        
        if training == 3:
            model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,
                                max_iter=epochs,  #run maar 1 epoch per keer dat we network.fit aanroepen
                                warm_start=True #ga verder met de gewichten van het netwerk uit de vorige network.fit (Als dit False was, werden de gewichten elke epoch weggegooit)
                                )


        model.fit(input_data_train[:num_data], labels_train[:num_data])
        with open(pkl_filename + str(num_data) + '.pkl', 'wb') as file:
              pickle.dump(model, file)
            
        #Bereken de MAE over de training data
        pred_labels = model.predict(input_data_train[:num_data])
        true_labels = labels_train[:num_data]
        train_acc = bereken_accuracy(pred_labels,true_labels)

        #Bereken de MAE over de test data
        pred_labels = model.predict(input_data_test[:1000])
        true_labels = labels_test[:1000]
        test_acc = bereken_accuracy(pred_labels,true_labels)

        train_accs.append(train_acc)
        test_accs.append(test_acc)

    #plot een aantal predictions en de MAE over de epochs 
    print(test_accs)
    plt.scatter(nums_data,train_accs,label='Train acc')
    plt.scatter(nums_data,test_accs,label='Test acc')
    plt.xlabel('#trianingdata')
    plt.ylabel('Accuracy')
    #plt.ylim(0,1)
    plt.legend()
    plt.show()

    for epoch_num in range(epochs):
        model.fit(input_data_train[:num_data], labels_train[:num_data])
        
        #Bereken de MAE over de training data
        pred_labels = model.predict(input_data_train[:num_data])
        true_labels = labels_train[:num_data]
        train_acc = bereken_accuracy(pred_labels,true_labels)
        train_accs.append(train_acc)

        #Bereken de MAE over de test data
        pred_labels = model.predict(input_data_test[:1000])
        true_labels = labels_test[:1000]
        test_acc = bereken_accuracy(pred_labels,true_labels)
        test_accs.append(test_acc)


    #plot een aantal predictions en de MAE over de epochs 

    plt.plot(train_accs,label='Train acc')
    plt.plot(test_accs,label='Test acc')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim(0,1)
    plt.legend()
    plt.show()

def results(model):
    pred_labels = model.predict(input_data_test)
    true_labels = labels_test

    MAE = bereken_MAE(pred_labels,true_labels)
    print('Het netwerk zit er gemiddeld {} naast.'.format(MAE))

    accuracy = bereken_accuracy(pred_labels,true_labels)
    print('Het netwerk heeft een nauwkeurigheid van {}.'.format(accuracy))

    dplot(true_labels,pred_labels,20)

    plot_confusion_matrix(model, input_data_test, labels_test,
                                    display_labels=['1','0'],
                                    cmap=plt.cm.Blues, values_format = '.0f')

try: # probeer het oude model te laden en maak anders een nieuw model
    with open(pkl_filename + '.pkl', 'rb') as file:
        model = pickle.load(file)

    results(model)
    
except:
    print('MLPRegressor(1) or LogisticRegression(2) or MLPClassifier(3)')
    training = int(input())
    if training == 1:
        hidden_layer_sizes = []
        while True:
            size = input('Grote van de (volgende) hidden layer: ')
            if size != '':
                try:
                    hidden_layer_sizes.append(int(size))
                except:
                    print('Size moet getal zijn')
            else:
                break
        epochs = input('Hoeveel epochs: ')
        print('training...')
        epoch(hidden_layer_sizes,epochs,1)

    elif training == 2:
        model = LogisticRegression()
        print('training...')
        model.fit(input_data_train,labels_train)

        with open(pkl_filename + '.pkl', 'wb') as file:
            pickle.dump(model, file)

        results(model)

    elif training == 3:
        hidden_layer_sizes = []
        while True:
            size = input('Grote van de (volgende) hidden layer: ')
            if size != '':
                try:
                    hidden_layer_sizes.append(int(size))
                except:
                    print('Size moet getal zijn')
            else:
                break
        epochs = input('Hoeveel epochs: ')
        print('training...')
        epoch(hidden_layer_sizes,epochs,3)