import PySimpleGUI as sg
import os.path
import pickle as pkl
import json


def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def window(model, input_values):
    settings = open_json()
    if settings["default save folder"] != "":
        text = settings["default save folder"]
    else:
        text = ""
    column = [
        [
            sg.Text("File name"),
            sg.In(size=(25, 1), key="file name")
        ],
        [
            sg.Text("Save folder"),
            sg.In(text, size=(25, 1), enable_events=True,
                  key="save folder", disabled=True),
            sg.FolderBrowse(),
        ],
        [
            sg.Button("Save", enable_events=True, key="save")
        ]

    ]
    save_layout = [
        [
            sg.Column(column)
        ]
    ]
    save_window = sg.Window("AI Creator", save_layout, icon=os.path.dirname(
        os.path.abspath(__file__)).replace("\\", "/") + "/Images/icon.ico").Finalize()

    while True:
        event, values = save_window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "save folder":
            save_window["save folder"].update(values["save folder"].split("/")[-1])

        if event == "save":
            file_name = values["file name"]
            save_path = values["save folder"]

            with open(save_path + "/" + file_name + ".model", 'wb') as file:
                pkl.dump(model, file)
            try:
                with open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/saved models/" + file_name, 'wb') as file:
                    pkl.dump(input_values, file)
            except:
                os.mkdir(os.path.dirname(os.path.abspath(__file__)
                                         ).replace("\\", "/") + "/saved models")
                with open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/saved models/" + file_name, 'wb') as file:
                    pkl.dump(input_values, file)

            save_window.close()
            break
