import PySimpleGUI as sg
import json
import csv
import pandas as pd
import zeroone


def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_json(file):
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
            "AI Creator", choose_data_layout).Finalize()

        while True:
            event, values = choose_data_window.read()
            if event == sg.WIN_CLOSED:
                break

            if event == "data":
                data_path = values["data"]
                if data_path != '':
                    file_name = data_path.split(
                        "/")[-1]  # Extract the file_name
                    # Create a dataframe of the file
                    df = pd.read_csv(data_path)
                    dataset = settings[file_name]
                    dataset.update({"datanodes": list(df)})
                    # All the values that need encoding will be encoded.
                    encode_columns = settings[file_name]["encode"]
                    df = zeroone.OHencoding(df, encode_columns)
                    datanodes = df.columns
                    label = settings[file_name]["label"]
                    dataset_values = []
                    for x in datanodes:
                        if x != label:
                            dataset_values.append(x)
                    for x in datanodes:
                        mapping = settings[file_name]["mapping"]
                        try:
                            settings[file_name]["mapping"][x]
                        except:
                            mapping.update({x: {"min": 0, "max": 1}})
                    settings.update({"dataset": data_path})
                    save_json(settings)
                    window.Close()
                    return datanodes, file_name, df, label, mapping, dataset_values
                else:
                    sg.PopupError("No data selected", title="Data error")

    else:
        data_path = settings["dataset"]  # Get the path of the dataset
        file_name = data_path.split("/")[-1]  # Extract the file_name
        df = pd.read_csv(data_path)  # Create a dataframe of the file
        dataset = settings[file_name]
        dataset.update({"datanodes": list(df)})
        # All the values that need encoding will be encoded.
        encode_columns = settings[file_name]["encode"]
        df = zeroone.OHencoding(df, encode_columns)
        datanodes = df.columns
        label = settings[file_name]["label"]
        dataset_values = []
        for x in datanodes:
            if x != label:
                dataset_values.append(x)
        for x in datanodes:
            mapping = settings[file_name]["mapping"]
            try:
                settings[file_name]["mapping"][x]
            except:
                mapping.update({x: {"min": 0, "max": 1}})
        settings.update({"dataset": data_path})
        save_json(settings)
        return datanodes, file_name, df, label, mapping, dataset_values
