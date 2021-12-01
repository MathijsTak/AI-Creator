import PySimpleGUI as sg
import pickle as pkl
from zeroone_ai import *
import columns
import save_window
import choose_data_window
import json

def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def save_json(file):
    theme_var = json.loads(str(file).replace("'", '"'))
    with open("settings.json", "w",) as write_file:
        json.dump(theme_var, write_file)

settings = open_json()
theme = settings["theme"]
themes = settings["themes"]
sg.theme(themes[theme]["theme"])
bgc = themes[theme]["bgc"]
tc = themes[theme]["tc"]

trainer = "MLPR"

menu_def = ['&File', ['New File', 'Open', 'Save', '---', 'Close']], ['Settings', ['Theme',
                                                                                  'Other Settings']], ['Train', ['Train', 'Epochtrain', '---', 'Plot']], ['Help', ['Help']]

while True:
    datanodes, file_name, data = choose_data_window.window()
    if file_name in settings:
        dataset_values = settings[file_name]["dataset_values"]
        label = settings[file_name]["label"]
        mapping = settings[file_name]["mapping"]
        break
    else:
        sg.PopupError("Data is not supported", title="Unsupported data")


# ----- menubar and columns -----

# Defining the layout for the window
while True:
    settings = open_json()
    theme = settings["theme"]
    themes = settings["themes"]
    sg.theme(themes[theme]["theme"])
    bgc = themes[theme]["bgc"]
    tc = themes[theme]["tc"]

    layout = [
        [
            sg.Menu(menu_def, background_color=bgc,
                    text_color=tc, font='verdana')
        ],
        [
            sg.Column(columns.home_column(), key="home", visible=True),
            sg.Column(columns.new_file_column(dataset_values, label),
                      key="new file", visible=False),
            sg.Column(columns.open_column(), key="open", visible=False),
            sg.Column(columns.theme_column(), key="theme", visible=False),
            sg.Column(columns.settings_column(),
                      key="settings", visible=False),

        ],
    ]

    # Creating window
    window = sg.Window("AI Creator", layout, resizable=True).Finalize()
    window.Maximize()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # ----- New file column -----
        # Training method
        if event == "mlpregressor":
            trainer = "MLPR"
            window["hidden layer sizes"].update("20,20,10", disabled=False)
            window["epochs"].update("200", disabled=False)
            window["num data"].update("2000", disabled=False)
        if event == "mlpclassifier":
            trainer = "MLPC"
            window["hidden layer sizes"].update("20,20,10", disabled=False)
            window["epochs"].update("200", disabled=False)
            window["num data"].update("2000", disabled=False)
        if event == "logisticregressor":
            trainer = "LR"
            window["hidden layer sizes"].update("", disabled=True)
            window["epochs"].update("", disabled=True)
            window["num data"].update("", disabled=True)

        # ----- Open file column -----
        if event == "open file":
            file_path = values["open file"]
            if file_path != '':
                with open(file_path, "rb") as file:
                    model = pkl.load(file)
                file_name = file_path.split("/")[-1]
                file_name = file_name.replace(".model", "")
                with open("C:/AI Creator/" + file_name, "rb") as file:
                    input_values = pkl.load(file)
                window["accuracy"].update(
                    str(model.accuracy * 100) + " %", visible=True)
                for x in dataset_values:
                    if x in input_values:
                        window[("input " + x)].update(disabled=False)
                    else:
                        window[("input " + x)].update("", disabled=True)
                window["predict"].update(disabled=False)

        if event == "predict":
            prediction_data = []
            for x in input_values:
                try:
                    prediction_data.append(int(values[("input " + x)]))
                except ValueError:
                    pass

            if len(prediction_data) == len(input_values):
                prediction_data = pd.DataFrame(
                    prediction_data, input_values).transpose()
                prediction = model.prediction(prediction_data)
                if prediction >= 0.75:
                    window["prediction"].update(
                        "Prediction: True (" + str(round((prediction[0] * 100), 1)) + "% chance)")
                elif prediction <= 0.5:
                    window["prediction"].update(
                        "Prediction: False (" + str(round((prediction[0] * 100), 1)) + "% chance)")
                else:
                    window["prediction"].update(
                        "Prediction: Not valid (" + str(round((prediction[0] * 100), 1)) + "% chance)")
            else:
                sg.PopupError("Input values have to be integers",
                              title="Invalid input values")

        # ----- Menu interaction -----
        # New file
        if event == "New File":
            window["home"].update(visible=False)
            window["new file"].update(visible=True)
            window["open"].update(visible=False)
            window["theme"].update(visible=False)
            window["settings"].update(visible=False)

        # Open
        if event == "Open":
            window["home"].update(visible=False)
            window["new file"].update(visible=False)
            window["open"].update(visible=True)
            window["theme"].update(visible=False)
            window["settings"].update(visible=False)

        # Save
        if event == "Save":
            try:
                model.accuracy
                save_window.window(model, input_values)
            except:
                sg.PopupError(
                    "No model has been trained or opened", title="No model")

        # Close
        if event == "Close":
            window["home"].update(visible=True)
            window["new file"].update(visible=False)
            window["open"].update(visible=False)
            window["theme"].update(visible=False)
            window["settings"].update(visible=False)

        # Theme
        if event == "Theme":
            window["home"].update(visible=False)
            window["new file"].update(visible=False)
            window["open"].update(visible=False)
            window["theme"].update(visible=True)
            window["settings"].update(visible=False)

        if event == 'Save setting':
            # wanneer wit
            for x in themes:
                if values[("-IN-", x)] == True:
                    settings.update({"theme": x})
                    save_json(settings)
            break

        # Other Settings
        if event == "Other Settings":
            window["home"].update(visible=False)
            window["new file"].update(visible=False)
            window["open"].update(visible=False)
            window["theme"].update(visible=False)
            window["settings"].update(visible=True)

        if event == "default save folder":
            settings.update(
                {"default save folder": values["default save folder"]})
            save_json(settings)

        if event == "remove default save folder":
            window["default save folder"].update("")
            settings.update(
                {"default save folder": ""})
            save_json(settings)

        if event == "data":
            data = values["data"]
            settings.update({"dataset": data})
            save_json(settings)
            break


        # Train
        if event == "Train":
            # Input values
            input_values = []
            for i in datanodes:
                try:
                    if values[i] == True:
                        input_values.append(i)
                except:
                    pass

            if input_values != []:
                # Hidden layer sizes
                hls = values["hidden layer sizes"].split(',')
                hidden_layer_sizes = []
                for x in hls:
                    try:
                        hidden_layer_sizes.append(int(x))
                    except:
                        pass

                if len(hidden_layer_sizes) > 0:
                    # Training
                    if trainer == "MLPR":
                        model = MLPRegressor(
                            data, input_values, label, mapping=mapping)
                        sg.PopupQuickMessage("Training...", font=("Any 20"))
                        model.train(hidden_layer_sizes)
                        sg.PopupQuickMessage("Done", font=("Any 20"))
                    if trainer == "MLPC":
                        model = MLPClassifier(
                            data, input_values, label, mapping=mapping)
                        sg.PopupQuickMessage("Training...", font=("Any 20"))
                        model.train(hidden_layer_sizes)
                        sg.PopupQuickMessage("Done", font=("Any 20"))

                    window["home"].update(visible=False)
                    window["new file"].update(visible=False)
                    window["open"].update(visible=True)
                    window["accuracy"].update(
                        str(model.accuracy * 100) + " %", visible=True)
                    for x in dataset_values:
                        if x in input_values:
                            window[("input " + x)].update(disabled=False)
                        else:
                            window[("input " + x)].update("", disabled=True)
                    window["predict"].update(disabled=False)
                elif trainer == "LR":
                    model = LogisticRegressor(
                        data, input_values, label, mapping=mapping)
                    sg.PopupQuickMessage("Training...", font=("Any 20"))
                    model.train()
                    sg.PopupQuickMessage("Done", font=("Any 20"))

                    window["home"].update(visible=False)
                    window["new file"].update(visible=False)
                    window["open"].update(visible=True)
                    window["accuracy"].update(
                        str(model.accuracy * 100) + " %", visible=True)
                    for x in dataset_values:
                        if x in input_values:
                            window[("input " + x)].update(disabled=False)
                        else:
                            window[("input " + x)].update("", disabled=True)
                    window["predict"].update(disabled=False)
                else:
                    sg.PopupError(
                        "Hidden layer sizes are not correctly filled in", title="Error")
            else:
                sg.PopupError("Select at least one input value", title="Error")

        # Epochtrain
        if event == "Epochtrain":
            sg.PopupQuickMessage(
                "This feature isn't available", font=("Any 20"))

        # Plot
        if event == "Plot":
            try:
                model.plot(length=20)
            except:
                sg.PopupError(
                    "No model has been trained or opened", title="No model")

        # Help
        if event == "Help":
            sg.PopupQuickMessage(
                "This feature isn't available", font=("Any 20"))

    window.Close()

    if event == sg.WIN_CLOSED:
        break

window.Close()