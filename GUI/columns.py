import PySimpleGUI as sg
import pickle as pkl
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


def menu():
    return ['&File', ['New File', 'Open', 'Save', '---', 'Close']], ['Settings', ['Theme',
                                                                                  'Other Settings']], ['Train', ['Train', 'Epochtrain', '---', 'Plot']], ['Help', ['Help']]


def home_column():
    column = [
        [
            sg.Text("To create an AI go to File and select New File")
        ],
        [
            sg.Text("Here you can set differend parameters for the AI")
        ],
        [
            sg.Text(
                "When the parameters are set, you can train the AI by going under Train and selecting Train")
        ],
        [
            sg.Text(
                "When done, you can predict with unknown data and save the file located under the File section")
        ],
        [
            sg.Text(
                "If you want more information on how to use the program see the Help section")
        ],
        [
            sg.Button("Github", key="github"),
            sg.Button("Buy me a coffee", key="coffee")
        ]
    ]
    return column


def new_file_column(dataset_values, label):
    checkboxes = [[]]
    for x in dataset_values:
        checkboxes[0].append(sg.Checkbox(x, default=False, key=x))

    # Defining menu and columns
    column = [
        [
            sg.Text("Input data", size=(10, 1)),
        ],
        [
            sg.Column(checkboxes, scrollable=True)
        ],
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


def open_column(dataset_values):
    column = [
        [
            sg.Text("Open file"),
            sg.In(disabled=True, enable_events=True, key="open file"),
            sg.FileBrowse(file_types=(("Model Files", ".model"),))
        ],
        [
            sg.Text("Mean absolute error:"),
            sg.Text("", visible=False, key="accuracy")
        ]
    ]

    for x in dataset_values:
        column.append([sg.Text(x, size=(20, 1)), sg.In(
            key=("input " + x), size=(15, 1), disabled=True)])

    column.append([sg.Button("Predict", disabled=True, key="predict")])
    column.append([sg.Text("Prediction: ", key="prediction")])

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


def settings_column(df_name):
    settings = open_json()
    old_df_columns = settings[df_name]["old_df_columns"]
    encode = settings[df_name]["encode"]
    label = settings[df_name]["df_label"]
    checkboxes = []
    for x in old_df_columns:
        if x in encode:
            checkboxes.append(sg.Checkbox(x, default=True, key=("encode", x)))
        else:
            checkboxes.append(sg.Checkbox(x, default=False, key=("encode", x)))
    settings = open_json()

    column = [
        [
            sg.Text("Default save folder", size=(20, 1)),
            sg.In(settings["default save folder"].split("/")[-1], size=(50, 1), enable_events=True,
                  key="default save folder", disabled=True),
            sg.FolderBrowse(),
            sg.Button("Remove", enable_events=True,
                      key="remove default save folder")
        ],
        [
            sg.Text("Dataset", size=(20, 1)),
            sg.In(settings["dataset"].split("/")[-1], size=(50, 1),
                  disabled=True, enable_events=True, key="data_path"),
            sg.FileBrowse(file_types=(("CSV Files", ".csv"),)),
        ],
        [
            sg.Text("Add/change dataset", size=(20, 1)),
            sg.In(size=(50, 1), disabled=True, enable_events=True, key="new data", visible=False),
            sg.FileBrowse(file_types=(("CSV Files", ".csv"),)),
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text("Values that need encoding"),
        ],
        checkboxes,
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text("Label"),
            sg.Combo(old_df_columns, key="new label", default_value=label)
        ],
        [
            sg.HorizontalSeparator()
        ],
        [
            sg.Text("Restart to save changes")
        ],
        [
            sg.Button("Restart", enable_events=True, key="Restart")
        ],
    ]

    return column
