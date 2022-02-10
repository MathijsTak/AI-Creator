import PySimpleGUI as sg
import json
import pandas as pd
import zeroone
import os
import add_data_window


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

                    while True:
                        settings = open_json()
                        if df_name in settings:
                            dataset = settings[df_name]
                        else:
                            new_data_path = values["data"]
                            new_df = pd.read_csv(new_data_path)
                            new_df_name = new_data_path.split("/")[-1]
                            new_df_columns = [
                                [
                                    sg.Text("Column name", size=(17, 1)),
                                    sg.Text("Min value", size=(15, 1)),
                                    sg.Text("Max value", size=(15, 1)),
                                    sg.Text("Encode value", size=(15, 1))
                                ]
                            ]
                            for x in list(new_df):
                                new_df_columns.append([sg.Text(x, size=(17, 1))])
                            counter = 1
                            for x in list(new_df):
                                new_df_columns[counter].append(sg.In(default_text=str(df[x].min()), key=("min", x), size=(17, 1)))
                                new_df_columns[counter].append(sg.In(default_text=str(df[x].max()), key=("max", x), size=(17, 1)))
                                new_df_columns[counter].append(sg.Checkbox("", key=("checkbox", x), size=(5, 1)))
                                new_df_columns[counter].append(sg.Text("", key=("error", x)))
                                counter += 1
                            new_df_columns.append([sg.Text("Label"), sg.Combo(list(new_df), key="new label")])

                            if add_data_window.window(new_df, new_df_columns, new_df_name) == True:
                                settings = open_json()
                                dataset = settings[df_name]
                                break
                        

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
                    return df_name, df, df_label, df_mapping, df_columns, data_path
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
        return df_name, df, df_label, df_mapping, df_columns, data_path
