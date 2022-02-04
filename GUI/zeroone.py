import numpy as np
from numpy.core.numeric import tensordot
import pandas as pd
import matplotlib.pyplot as matplot
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor as MLPR
from sklearn.linear_model import LogisticRegression as LR
from sklearn.neural_network import MLPClassifier as MLPC


def OHencoding(df, columns):
    for column in columns:
        df = pd.get_dummies(df, columns=[column], prefix=[column])
    return df


def accuracy(pred_labels, true_labels):
    all_errors = []
    for pred_label, true_label in zip(pred_labels, true_labels):
        # in elke iteratie van de loop krijgen we 1 predicted label in pred_label en 1 bijbehorend true label in true_label

        absolute_error = abs(pred_label - true_label)

        all_errors.append(absolute_error)

    MAE = sum(all_errors) / len(all_errors)
    return MAE


def normalize(df, mapping):
    result = df.copy()
    for feature_name in df.columns:
        max_value = mapping[feature_name]['max']
        min_value = mapping[feature_name]['min']
        result[feature_name] = (
            df[feature_name] - min_value) / (max_value - min_value)
    return result


def plt(true_labels, pred_labels, label, length, yrange, ax):
    if ax == None:
        fig, ax = matplot.subplots()
    index = np.arange(length)
    bar_width = 0.25
    opacity = 0.8

    rects1 = ax.bar(index, true_labels[:length], bar_width,
                    alpha=opacity, color='r', label='True_labels')
    rects2 = ax.bar(index + bar_width, pred_labels[:length],
                    bar_width, alpha=opacity, color='b', label='Pred_labels')
    rects2 = ax.bar(index + 2*bar_width, abs(true_labels[:length]-pred_labels[:length]),
                    bar_width, alpha=opacity, color='g', label='Absolute Error')
    ax.ticklabel_format(style='plain')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(label)
    if yrange != None:
        ax.set_ylim(yrange)
    ax.legend()

    if ax == None:
        matplot.show()

    matplot.show()


class MLPRegressor:
    def __init__(self, dataset, input_data, label, test_size=0.2, random_state=42, mapping=None):
        self.label = label
        self.mapping = mapping
        input_data = dataset[input_data]
        if mapping == None:
            input_data = (input_data - input_data.mean()) / \
                (input_data.max() - input_data.min())
            self.mean = input_data.mean()
            self.max = input_data.max()
            self.min = input_data.min()
        else:
            input_data = normalize(input_data, mapping)
        label = dataset[self.label]

        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(
            input_data, label, test_size=test_size, random_state=random_state)

    def plot(self, length, yrange=None, ax=None):
        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        pred_labels = np.round(np.clip(pred_labels,0,1))

        plt(true_labels, pred_labels, self.label, length, yrange, ax)

    def prediction(self, prediction_data):
        if self.mapping == None:
            prediction_data = (prediction_data - self.mean) / \
                (self.max - self.min)
        else:
            prediction_data = normalize(prediction_data, self.mapping)
        pred_label = self.model.predict(prediction_data)
        return pred_label

    def train(self, hidden_layer_sizes):
        self.model = MLPR(hidden_layer_sizes)
        self.model.fit(self.data_train, self.labels_train)

        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        pred_labels = np.round(np.clip(pred_labels,0,1))

        self.accuracy = accuracy(pred_labels, true_labels)
        print('Het model heeft een nauwkeurigheid van {}.'.format(self.accuracy))

    def epochtrain(self, hidden_layer_sizes, epochs, num_data):
        self.model = MLPR(hidden_layer_sizes, max_iter=1, warm_start=True)

        train_accs = []
        test_accs = []

        for epoch in range(epochs):
            self.model.fit(
                self.data_train[:num_data], self.labels_test[:num_data])

            pred_labels = self.model.predict(self.data_train[:num_data])
            true_labels = self.labels_train[:num_data]
            train_acc = accuracy(pred_labels, true_labels)
            train_accs.append(train_acc)

            pred_labels = self.model.predict(self.data_test[:1000])
            true_labels = self.labels_test[:1000]
            test_acc = accuracy(pred_labels, true_labels)
            test_accs.append(test_acc)

        matplot.plot(train_accs, label='Train acc')
        matplot.plot(test_accs, label='Test acc')
        matplot.xlabel('Epoch')
        matplot.ylabel('Accuracy')
        matplot.ylim(0.1)
        matplot.legend()
        matplot.plot()
        matplot.show()


class MLPClassifier:
    def __init__(self, dataset, input_data, label, test_size=0.2, random_state=42, mapping=None):
        self.label = label
        self.mapping = mapping
        input_data = dataset[input_data]
        if mapping == None:
            input_data = (input_data - input_data.mean()) / \
                (input_data.max() - input_data.min())
            self.mean = input_data.mean()
            self.max = input_data.max()
            self.min = input_data.min()
        else:
            input_data = normalize(input_data, mapping)
        label = dataset[self.label]

        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(
            input_data, label, test_size=test_size, random_state=random_state)

    def plot(self, length, yrange=None, ax=None):
        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        #pred_labels = np.round(np.clip(pred_labels,0,1))

        plt(true_labels, pred_labels, self.label, length, yrange, ax)

    def prediction(self, prediction_data):
        if self.mapping == None:
            prediction_data = (prediction_data - self.mean) / \
                (self.max - self.min)
        else:
            prediction_data = normalize(prediction_data, self.mapping)
        pred_label = self.model.predict(prediction_data)
        return pred_label

    def train(self, hidden_layer_sizes):
        self.model = MLPC(hidden_layer_sizes)
        self.model.fit(self.data_train, self.labels_train)

        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        #pred_labels = np.round(np.clip(pred_labels,0,1))

        self.accuracy = accuracy(pred_labels, true_labels)
        print('Het model heeft een nauwkeurigheid van {}.'.format(self.accuracy))

    def epochtrain(self, hidden_layer_sizes, epochs, num_data):
        self.model = MLPC(hidden_layer_sizes, max_iter=1, warm_start=True)

        train_accs = []
        test_accs = []

        for epoch in range(epochs):
            self.model.fit(
                self.data_train[:num_data], self.labels_test[:num_data])

            pred_labels = self.model.predict(self.data_train[:num_data])
            true_labels = self.labels_train[:num_data]
            train_acc = accuracy(pred_labels, true_labels)
            train_accs.append(train_acc)

            pred_labels = self.model.predict(self.data_test[:1000])
            true_labels = self.labels_test[:1000]
            test_acc = accuracy(pred_labels, true_labels)
            test_accs.append(test_acc)

        matplot.plot(train_accs, label='Train acc')
        matplot.plot(test_accs, label='Test acc')
        matplot.xlabel('Epoch')
        matplot.ylabel('Accuracy')
        matplot.ylim(0.1)
        matplot.legend()
        matplot.plot()
        matplot.show()


class LogisticRegressor:
    def __init__(self, dataset, input_data, label, test_size=0.2, random_state=42, mapping=None):
        self.label = label
        self.mapping = mapping
        input_data = dataset[input_data]
        if mapping == None:
            input_data = (input_data - input_data.mean()) / \
                (input_data.max() - input_data.min())
            self.mean = input_data.mean()
            self.max = input_data.max()
            self.min = input_data.min()
        else:
            input_data = normalize(input_data, mapping)
        label = dataset[self.label]

        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(
            input_data, label, test_size=test_size, random_state=random_state)

    def plot(self, length, yrange=None, ax=None):
        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        #pred_labels = np.round(np.clip(pred_labels,0,1))

        plt(true_labels, pred_labels, self.label, length, yrange, ax)

    def prediction(self, prediction_data):
        if self.mapping == None:
            prediction_data = (prediction_data - self.mean) / \
                (self.max - self.min)
        else:
            prediction_data = normalize(prediction_data, self.mapping)
        pred_label = self.model.predict(prediction_data)
        return pred_label

    def train(self):
        self.model = LR()
        self.model.fit(self.data_train, self.labels_train)

        pred_labels = self.model.predict(self.data_test)
        true_labels = self.labels_test
        #pred_labels = np.round(np.clip(pred_labels,0,1))

        self.accuracy = accuracy(pred_labels, true_labels)
        print('Het model heeft een nauwkeurigheid van {}.'.format(self.accuracy))
