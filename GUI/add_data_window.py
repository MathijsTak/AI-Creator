import PySimpleGUI as sg
import json
import csv
import pandas as pd
import zeroone
import os

def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_json(file, position, update):
    position.update(update)
    theme_var = json.loads(str(file).replace("'", '"'))
    with open("settings.json", "w",) as write_file:
        json.dump(theme_var, write_file)

def window(df, df_columns, df_name):
    settings = open_json()
    column = [
        
        [
            sg.Column(df_columns, scrollable=True, size=(1000,500)),
        ],
        [
            sg.Button("Add", enable_events=True, key="add dataset")
        ],
    ]

    add_data_layout = [
        [
            sg.Column(column)
        ]
    ]

    add_data_window = sg.Window("AI Creator", add_data_layout, icon=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/Images/icon.ico").Finalize()

    while True:
        event, values = add_data_window.read()
        if event == sg.WIN_CLOSED:
            return False

        if event == "add dataset":
            save_json(settings, settings, {df_name: {}})

            encode_columns = []
            for x in list(df):
                if values[("checkbox", x)] == True:
                    encode_columns.append(x)
            save_json(settings, settings[df_name], {"encode": encode_columns})

            new_label = values["new label"]
            save_json(settings, settings[df_name], {"df_label": new_label})

            save_json(settings, settings[df_name], {"df_mapping": {}})

            error = []
            for x in list(df):
                try:
                    min = float(values[("min", x)])
                    max = float(values[("max", x)])
                except:
                    min = 0
                    max = 1
                    error.append(x)
                save_json(settings, settings[df_name]["df_mapping"], {x: {"min": min, "max": max}})
