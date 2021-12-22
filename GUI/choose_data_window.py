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


def window():
    settings = open_json()
    if settings["dataset"] == "":
        column = [
            [
                sg.Text("Data", size=(10, 1)),
                sg.In(size=(25, 1), disabled=True,
                      enable_events=True, key="data"),
                sg.FileBrowse(file_types=(("CSV Files", ".csv"),)),
            ],
        ]

        choose_data_layout = [
            [
                sg.Column(column)
            ]
        ]

        choose_data_window = sg.Window(
            "AI Creator", choose_data_layout, icon=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/Images/icon.ico").Finalize()

        while True:
            event, values = choose_data_window.read()
            if event == sg.WIN_CLOSED:
                return False

            if event == "data":
                data_path = values["data"]
                if data_path != '':
                    df_name = data_path.split(
                        "/")[-1]  # Extract the df_name
                    # Create a dataframe of the file
                    df = pd.read_csv(data_path)
                    dataset = settings[df_name]
                    dataset.update({"old_df_columns": list(df)})
                    # All the values that need encoding will be encoded.
                    encode_columns = settings[df_name]["encode"]
                    df = zeroone.OHencoding(df, encode_columns)
                    df_label = settings[df_name]["df_label"]
                    df_columns = []
                    for x in list(df):
                        if x != df_label:
                            df_columns.append(x)
                    for x in list(df):
                        df_mapping = settings[df_name]["df_mapping"]
                        try:
                            df_mapping[x]
                        except:
                            save_json(settings, df_mapping, {
                                      x: {"min": 0, "max": 1}})
                    save_json(settings, settings, {"dataset": data_path})
                    choose_data_window.Close()
                    return df_name, df, df_label, df_mapping, df_columns
                else:
                    sg.PopupError("No data selected", title="Data error")

    else:
        data_path = settings["dataset"]  # Get the path of the dataset
        df_name = data_path.split("/")[-1]  # Extract the df_name
        df = pd.read_csv(data_path)  # Create a dataframe of the file
        dataset = settings[df_name]
        save_json(settings, dataset, {"old_df_columns": list(df)})
        # All the values that need encoding will be encoded.
        encode_columns = settings[df_name]["encode"]
        df = zeroone.OHencoding(df, encode_columns)
        df_label = settings[df_name]["df_label"]
        df_columns = []
        for x in list(df):
            if x != df_label:
                df_columns.append(x)
        for x in list(df):
            df_mapping = settings[df_name]["df_mapping"]
            try:
                settings[df_name]["df_mapping"][x]
            except:
                save_json(settings, df_mapping, {x: {"min": 0, "max": 1}})
        save_json(settings, settings, {"dataset": data_path})
        return df_name, df, df_label, df_mapping, df_columns
