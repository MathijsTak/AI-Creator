import PySimpleGUI as sg
import pickle as pkl
import zeroone
from zeroone import *
import columns
import save_window
import choose_data_window
import add_data_window
import json
import webbrowser
import os

# Basic functions to load and save the settings.json file

def open_json():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_json(file, position, update):
    position.update(update)
    theme_var = json.loads(str(file).replace("'", '"'))
    with open("settings.json", "w",) as write_file:
        json.dump(theme_var, write_file)

def save_dataset():
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
            settings[df_name]["df_mapping"][x]
        except:
            save_json(settings, df_mapping, {
                        x: {"min": 0, "max": 1}})

    save_json(settings, settings, {"dataset": data_path})

def save_encode(df_name, dataset):
    old_df_columns = settings[df_name]["old_df_columns"]
    encode_columns = []
    for i in old_df_columns:
        if values[("encode", i)] == True:
            encode_columns.append(i)
    save_json(settings, dataset, {"encode": encode_columns})

def save_label(dataset):
            new_label = values["new label"]
            save_json(settings, dataset, {"df_label": new_label})

def autosave(model, input_values, settings):
    save_path = settings["default save folder"]
    if save_path != "":
        x = ""
        i = 1
        try:
            while True:
                with open(save_path + "/" + str(input_values) + "-autosave" + x + ".model", 'rb') as file:
                    pkl.load(file)
                x = "(" + str(i) + ")"
                i += 1
        except:
            with open(save_path + "/" + str(input_values) + "-autosave" + x + ".model", 'wb') as file:
                pkl.dump(model, file)
            try:
                with open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/saved models/" + str(input_values) + "-autosave" + x, 'wb') as file:
                    pkl.dump(input_values, file)
            except:
                os.mkdir(os.path.dirname(os.path.abspath(__file__)
                                        ).replace("\\", "/") + "/saved models")
                with open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/saved models/" + str(input_values) + "-autosave" + x, 'wb') as file:
                    pkl.dump(input_values, file)


# Some starting variabled to run the program
trainer = "MLPR"
df_name = None

while True:
    if choose_data_window.window() == False:  # If user closes the program on first startup close the whole program
        break
    # Let the user pick a dataset and then save the dataset information
    df_name, df, df_label, df_mapping, df_columns, data_path = choose_data_window.window()
    settings = open_json()

    # Retrieving the currend theme of the program
    theme = settings["theme"]
    themes = settings["themes"]
    sg.theme(themes[theme]["theme"])
    bgc = themes[theme]["bgc"]
    tc = themes[theme]["tc"]

    # Creating the layout for the program
    layout = [
        [
            sg.Menu(columns.menu(), background_color=bgc,
                    text_color=tc, font='verdana')
        ],
        [
            sg.Column(columns.home_column(), key="home", visible=True),
            sg.Column(columns.new_file_column(df_columns, df_label),
                      key="new file", visible=False),
            sg.Column(columns.open_column(df_columns),
                      key="open", visible=False),
            sg.Column(columns.theme_column(), key="theme", visible=False),
            sg.Column(columns.settings_column(df_name),
                      key="settings", visible=False),

        ],
    ]

    # Creating window
    window = sg.Window("AI Creator", layout, resizable=True,
                       icon=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/Images/icon.ico").Finalize()
    window.Maximize()

    # Start the window
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:  # If user closes program close program
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
                model_name = file_path.split("/")[-1]
                model_name = model_name.replace(".model", "")
                with open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/saved models/" + model_name, "rb") as file:
                    input_values = pkl.load(file)
                window["accuracy"].update(
                    str(model.accuracy), visible=True)
                for x in df_columns:
                    if x in input_values:
                        window[("input " + x)].update(disabled=False)
                    else:
                        window[("input " + x)].update("", disabled=True)
                window["predict"].update(disabled=False)

        if event == "predict":
            prediction_data = []
            for x in input_values:
                try:
                    prediction_data.append(float(values[("input " + x)]))
                except ValueError:
                    pass

            if len(prediction_data) == len(input_values):
                prediction_data = pd.DataFrame(
                    prediction_data, input_values).transpose()
                prediction = model.prediction(prediction_data)
                window["prediction"].update("Prediction: " + str(prediction))
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
            for x in themes:
                if values[("-IN-", x)] == True:
                    save_json(settings, settings, {"theme": x})
            break

        # Other Settings
        if event == "Other Settings":
            window["home"].update(visible=False)
            window["new file"].update(visible=False)
            window["open"].update(visible=False)
            window["theme"].update(visible=False)
            window["settings"].update(visible=True)

        if event == "default save folder":
            save_json(
                settings, settings, {"default save folder": values["default save folder"]})
            save_folder = values["default save folder"].split("/")[-1]
            window["default save folder"].update(save_folder)

        if event == "remove default save folder":
            window["default save folder"].update("")
            save_json(settings, settings, {"default save folder": ""})

        if event == "data_path":
            old_data_path = data_path
            data_path = values["data_path"]
            if data_path != old_data_path:
                local_df_name = data_path.split("/")[-1]
                print(local_df_name)
                if local_df_name not in settings:
                    sg.PopupError("Data is not supported",
                                  title="Unsupported data")
                else:
                    window["data_path"].update(local_df_name)
            else:
                sg.PopupError(
                    "No data selected or same data selected", title="Data error")
        
        if event == "new data":
            new_data_path = values["new data"]
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
                new_df_columns[counter].append(sg.In(default_text=str(new_df[x].min()), key=("min", x), size=(17, 1)))
                new_df_columns[counter].append(sg.In(default_text=str(new_df[x].max()), key=("max", x), size=(17, 1)))
                new_df_columns[counter].append(sg.Checkbox("", key=("checkbox", x), size=(5, 1)))
                new_df_columns[counter].append(sg.Text("", key=("error", x)))
                counter += 1
            new_df_columns.append([sg.Text("Label"), sg.Combo(list(new_df), key="new label")])

            add_data_window.window(new_df, new_df_columns, new_df_name)

        if event == "Restart":
            dataset = settings[df_name]
            save_encode(df_name, dataset)
            save_label(dataset)
            save_dataset()
            break

        # Add dataset
        if event == "Add dataset":
            sg.PopupError(title="Feature comming soon")

        # Train
        if event == "Train":
            settings = open_json()
            # Input values
            input_values = []
            for i in list(df):
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
                            df, input_values, df_label, mapping=df_mapping)
                        sg.PopupQuickMessage("Training...", font=("Any 20"))
                        model.train(hidden_layer_sizes)
                        sg.PopupQuickMessage("Done", font=("Any 20"))
                    if trainer == "MLPC":
                        model = MLPClassifier(
                            df, input_values, df_label, mapping=df_mapping)
                        sg.PopupQuickMessage("Training...", font=("Any 20"))
                        model.train(hidden_layer_sizes)
                        sg.PopupQuickMessage("Done", font=("Any 20"))

                    window["home"].update(visible=False)
                    window["new file"].update(visible=False)
                    window["open"].update(visible=True)
                    window["accuracy"].update(
                        str(model.accuracy), visible=True)
                    for x in df_columns:
                        if x in input_values:
                            window[("input " + x)].update(disabled=False)
                        else:
                            window[("input " + x)].update("", disabled=True)
                    window["predict"].update(disabled=False)
                    autosave(model, input_values, settings)
                elif trainer == "LR":
                    model = LogisticRegressor(
                        df, input_values, df_label, mapping=df_mapping)
                    sg.PopupQuickMessage("Training...", font=("Any 20"))
                    model.train()
                    sg.PopupQuickMessage("Done", font=("Any 20"))

                    window["home"].update(visible=False)
                    window["new file"].update(visible=False)
                    window["open"].update(visible=True)
                    window["accuracy"].update(
                        str(model.accuracy), visible=True)
                    for x in df_columns:
                        if x in input_values:
                            window[("input " + x)].update(disabled=False)
                        else:
                            window[("input " + x)].update("", disabled=True)
                    window["predict"].update(disabled=False)
                    autosave(model, input_values, settings)
                else:
                    sg.PopupError(
                        "Hidden layer sizes are not correctly filled in", title="Error")
            else:
                sg.PopupError("Select at least one input value", title="Error")

        # Epochtrain
        if event == "Epochtrain":
            # Input values
            input_values = []
            for i in list(df):
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
                    epochs = values["epochs"]
                    try:
                        epochs = int(epochs)
                    except:
                        pass

                    if isinstance(epochs, int) == True:
                        num_data = values["num data"]
                        try:
                            num_data = int(num_data)
                        except:
                            pass

                        if isinstance(num_data, int) == True:
                            if trainer == "MLPR":
                                model = MLPRegressor(
                                    df, input_values, df_label, df_mapping=df_mapping)
                            elif trainer == "MLPC":
                                model = MLPClassifier(
                                    df, input_values, df_label, df_mapping=df_mapping)
                            elif trainer == "LR":
                                model = LogisticRegressor(
                                    df, input_values, df_label, df_mapping=df_mapping)

                            sg.PopupQuickMessage(
                                "Training...", font=("Any 20"))
                            model.epochtrain(
                                hidden_layer_sizes, epochs, num_data)
                            sg.PopupQuickMessage("Done", font=("Any 20"))

                        else:
                            sg.PopupError(
                                "Number of data has to be an integer", title="Error")
                    else:
                        sg.PopupError(
                            "Epochs has to be an integer", title="Error")
                else:
                    sg.PopupError(
                        "Hidden layer sizes are not correctly filled in", title="Error")
            else:
                sg.PopupError("Select at least one input value", title="Error")

        # Plot
        if event == "Plot":
            try:
                model.plot(length=20)
            except:
                sg.PopupError(
                    "No model has been trained or opened", title="No model")

        # Help
        if event == "Help":
            webbrowser.open(
                "https://github.com/MathijsTak/Pacemaker-ai/blob/main/README.md#product")

        if event == "github":
            webbrowser.open("https://github.com/MathijsTak/Pacemaker-ai")

        if event == "coffee":
            webbrowser.open("https://www.buymeacoffee.com/MathijsTak")

    window.Close()

    if event == sg.WIN_CLOSED:
        break
if df_name != None:
    window.Close()
