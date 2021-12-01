Knowledge required for this programm
- You know how an AI is trained

Installation
- Download the latest realease
- Extract the zip file on your computer

How to use
- Open the file named 'AI Creator.exe'
- When the programm starts you need to select the dataset (csv file) you want to use. (This has to be one of the datasets given below)
- To create an AI go to File and select New File
- Here you can set differend parameters for the AI
- When the parameters are set, you can train the AI by going under Train and selecting Train
- When done, you can predict with unkown data and save the file located under the File section

Settings
- In settings.json are all the available datasets listed and it is posible to add a dataset yourself.
- You can do this by sorting all the lines. I use a VS Code extension for this, and then add your dataset with the input_values, label and mapping
- To change the default save folder and the dataset you can either edit the settings.json or inside the application under Settings and then Other Settings.


Work in progress
- Epochtrain together with the epochs and number of data is not available at the moment
- Auto save and auto open option in the other settings menu
- Change the dataset in the other settings menu

Idea's
- Ability to add new datasets in the programm (now you have to edit the settings.json file and the python file in order to add a new dataset)
- Ability to change the mapping for the datasets
