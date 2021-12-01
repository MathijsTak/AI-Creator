import PySimpleGUI as sg
import os.path
import pickle as pkl
import csv
from tkinter.constants import X
from typing import Text
from PySimpleGUI.PySimpleGUI import I
from matplotlib.pyplot import fill_betweenx
from zeroone_ai import *
import json


def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def save_json(file):
    theme_var = json.loads(str(file).replace("'", '"'))
    with open("settings.json", "w",) as write_file:
        json.dump(theme_var, write_file)


def getcolumns(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_column_names = []
        for row in csv_reader:
            list_of_column_names.append(row)
            break

    return list_of_column_names[0]


def home_column():
    column = [
        [
            sg.Text("Welkom!"),
        ]
    ]
    return column


def new_file_column(dataset_values, label):
    checkboxes = []
    for x in dataset_values:
        checkboxes.append(sg.Checkbox(x, default=False, key=x))

    # Defining menu and columns
    column = [
        [
            sg.Text("Input data", size=(10, 1)),
        ],
        checkboxes,
        [
            sg.Text("Label: " + label, size=(15, 1)),
        ],
        [
            sg.HSeparator()
        ],
        [
            sg.Radio("MLPRegressor", "group", size=(15, 2), default=True,
                     enable_events=True, key="mlpregressor"),
            sg.Radio("MLPClassifier", "group", size=(15, 2),
                     enable_events=True, key="mlpclassifier"),
            sg.Radio("LogisticRegressor", "group", size=(15, 2),
                     enable_events=True, key="logisticregressor"),
        ],
        [
            sg.Text("Hidden layer sizes", size=(20, 1)),
            sg.InputText("20,20,10", disabled=False, size=(
                25, 1), key="hidden layer sizes")
        ],
        [
            sg.Text("Epochs", size=(20, 1)),
            sg.InputText("200", size=(25, 1), disabled=False, key="epochs")
        ],
        [
            sg.Text("Number of data", size=(20, 1)),
            sg.InputText("2000", size=(25, 1), disabled=False, key="num data")
        ],
        [
            sg.HSeparator()
        ]
    ]

    return column


def open_column():
    column = [
        [
            sg.Text("Open file"),
            sg.In(disabled=True, enable_events=True, key="open file"),
            sg.FileBrowse(file_types=(("Model Files", ".model"),))
        ],
        [
            sg.Text("Model accuracy:"),
            sg.Text("", visible=False, key="accuracy")
        ],
        [
            sg.Text("age", size=(10, 1)),
            sg.In(key=("input age"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("gender", size=(10, 1)),
            sg.In(key=("input gender"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("height", size=(10, 1)),
            sg.In(key=("input height"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("weight", size=(10, 1)),
            sg.In(key=("input weight"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("ap_hi", size=(10, 1)),
            sg.In(key=("input ap_hi"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("ap_lo", size=(10, 1)),
            sg.In(key=("input ap_lo"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("cholesterol", size=(10, 1)),
            sg.In(key=("input cholesterol"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("gluc", size=(10, 1)),
            sg.In(key=("input gluc"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("smoke", size=(10, 1)),
            sg.In(key=("input smoke"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("alco", size=(10, 1)),
            sg.In(key=("input alco"), size=(10, 1), disabled=True)
        ],
        [
            sg.Text("active", size=(10, 1)),
            sg.In(key=("input active"), size=(10, 1), disabled=True)
        ],
        [
            sg.Button("Predict", disabled=True, key="predict")
        ],
        [
            sg.Text("Prediction: ", key="prediction")
        ]
    ]

    return column

def theme_column():
    settings = open_json()
    column = [
        [
            sg.Text("Theme Settings")
        ]
    ]
    theme = settings["theme"]
    themes = settings["themes"]

    for x in themes:
        if x == theme:
            default = True
        else:
            default = False
        column.append([sg.Radio(themes[x]["name"], "RADIO1",
                      default=default, key=("-IN-", x))])

    column.append([sg.Button("Save setting")])

    return column


def settings_column():
    settings = open_json()

    column = [
        [
            sg.Text("Default save folder"),
            sg.In(settings["default save folder"], size=(25, 1), enable_events=True,
                  key="default save folder", disabled=True),
            sg.FolderBrowse(),
            sg.Button("Remove", enable_events=True,
                      key="remove default save folder")
        ],
        [
            sg.Text("Data", size=(10, 1)),
            sg.In(settings["dataset"], size=(25, 1), disabled=True, enable_events=True, key="data"),
            sg.FileBrowse(file_types=(("CSV Files", ".csv"),)),
        ],
    ]

    return column
