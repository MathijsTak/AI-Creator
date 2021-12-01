# Pacemaker AI

## Table of contents
- Preface
- Introduction
- Description of what is already known
- Own research
  - Installation
  - How to use
  - Settings
  - Work in progress
  - Idea's
- Conclusion
- Reflexion
- Citation

## Preface
With this program we try to predict heart failure. 

## Introduction

## Description of what is already known
- You know how an AI is trained

## Own research

### Installation
- Download the latest realease
- Extract the zip file on your computer

### How to use
- Open the file named 'AI Creator.exe'
- When the programm starts you need to select the dataset (csv file) you want to use. (This has to be one of the datasets given below)
- To create an AI go to File and select New File
- Here you can set differend parameters for the AI
- When the parameters are set, you can train the AI by going under Train and selecting Train
- When done, you can predict with unkown data and save the file located under the File section

### Settings
- In settings.json are all the available datasets listed and it is posible to add a dataset yourself.
- You can do this by sorting all the lines. I use a VS Code extension for this, and then add your dataset with the input_values, label and mapping
- To change the default save folder and the dataset you can either edit the settings.json or inside the application under Settings and then Other Settings.


### Work in progress
- Epochtrain together with the epochs and number of data is not available at the moment
- Auto save and auto open option in the other settings menu
- Change the dataset in the other settings menu

### Idea's
- Ability to add new datasets in the programm (now you have to edit the settings.json file and the python file in order to add a new dataset)
- Ability to change the mapping for the datasets

## Conclusion

## Reflection

## Citation
- scikit-learn (new BSD) https://pypi.org/project/scikit-learn/
- pandas (BSD 3-Clause License) https://github.com/pandas-dev/pandas/blob/master/LICENSE
- matplotlib (Python Software Foundation License (PSF)) https://pypi.org/project/matplotlib/3.4.3/
- numpy (BSD License (BSD)) https://github.com/numpy/numpy/blob/main/LICENSE.txt
- zeroone-ai (MIT) https://github.com/MathijsTak/ZeroOneAi
- PySimpleGUI (GNU Lesser General Public License v3.0) https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt
