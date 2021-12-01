import PySimpleGUI as sg
import json
import csv

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

def window():
    settings = open_json()
    if settings["dataset"] == "":
        column = [
            [
                sg.Text("Data", size=(10, 1)),
                sg.In(size=(25, 1), disabled=True, enable_events=True, key="data"),
                sg.FileBrowse(file_types=(("CSV Files", ".csv"),)),
            ],
        ]

        choose_data_layout = [
            [
                sg.Column(column)
            ]
        ]

        choose_data_window = sg.Window("AI Creator", choose_data_layout).Finalize()

        while True:
            event, values = choose_data_window.read()
            if event == sg.WIN_CLOSED:
                break

            if event == "data":
                data = values["data"]
                settings.update({"dataset": data})
                save_json(settings)
                if data != '':
                    datanodes = getcolumns(data)
                    file_name = data.split("/")[-1]
                    print(file_name)
                    choose_data_window.Close()
                    return datanodes, file_name, data
                else:
                    sg.PopupError("No data selected", title="Data error")

    else:
        data = settings["dataset"]
        datanodes = getcolumns(data)
        file_name = data.split("/")[-1]
        print(file_name)
        return datanodes, file_name, data