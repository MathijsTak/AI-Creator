# Pacemaker AI

## Table of contents
- [Preface](https://github.com/MathijsTak/Pacemaker-ai#preface)
- [Introduction](https://github.com/MathijsTak/Pacemaker-ai#introduction)
- [Description of what is already known](https://github.com/MathijsTak/Pacemaker-ai#description-of-what-is-already-known)
  - What is an AI
- [Own research](https://github.com/MathijsTak/Pacemaker-ai#own-research)
- [Product](https://github.com/MathijsTak/Pacemaker-ai/blob/main/README.md#product)
  - Installation
  - How to use
  - Available datasets
  - Settings
- [Conclusion](https://github.com/MathijsTak/Pacemaker-ai#conclusion)
- [Reflexion](https://github.com/MathijsTak/Pacemaker-ai#reflection)
- [Citation](https://github.com/MathijsTak/Pacemaker-ai#citation)

## Preface
With this program we try to predict heart failure. 

## Introduction
Heart failure is one of the most common causes of death. Those affected often aren't aware they are at risk. With this program we try to show people whether it is likely that they will develop heart failure. Hopefully the program can stimulate more people to go see a doctor wwhen necessary. This mighth result in less deaths caused by heart failure. 

## Description of what is already known
### What is an AI
Artificial Intelligence (AI) is really nothing more than a computer trying to imitate human intelligence. AI includes Machine Learning and deep learning. Both can be used for different purposes. For example, deep learning will work better if more data is available. Because processing this large amount of data requires a high-end machine.

A machine learning model consists of neurons and weights. While learning, the computer will adjust these weights to get a higher accuracy. The neurons are divided into three categories the input layer, hidden layer, and the output layer. The input layer is your input values, and the output layer is the prediction. The hidden layers can be adjusted to get better accuracy. 

For more information on how a neural network works click [here](https://www.ibm.com/cloud/learn/neural-networks)


## Own research
To know more about heart failure, we did some research on the heart. We learned how to heart functions and how heart failure can arise. To read more about the research we did, click [here](https://github.com/MathijsTak/Pacemaker-ai/raw/main/The%20heart.docx)  

## Product
We made a program that is able to create and train a model and then predict unknown data

### Installation
- Download the latest realease
- Extract the zip file on your computer

### How to use
- Open the file named 'Pacemaker AI.exe'
- When the program starts for the first time you need to select the dataset (csv file) you want to use. (This has to be one of the datasets given below)
- To create an AI go to File and select New File
- Here you can set differend parameters for the AI
- When the parameters are set, you can train the AI by going under Train and selecting Train
- When done, you can predict with unknown data and save the file located under the File section
- If you want more information on how to use the program see the Wiki

### Available datasets
- https://www.kaggle.com/sulianova/cardiovascular-disease-dataset
- https://www.kaggle.com/andrewmvd/heart-failure-clinical-data
- Note: You can [add other datasets](https://github.com/MathijsTak/Pacemaker-ai/wiki/settings.json) in 'Settings.json'

### Settings
- In settings.json are all the available datasets listed and it is posible to add a dataset yourself.
- You can do this by sorting all the lines. I use a VS Code extension for this, and then add your dataset with the input_values, label and mapping
- To change the default save folder and the dataset you can either edit the settings.json or inside the application under Settings and then Other Settings.

[Project board](https://github.com/MathijsTak/Pacemaker-ai/projects/1?fullscreen=true)


## Conclusion
We made a functioning AI that can predict heartfailure. However, the AI is very basic and only uses 10 different variabeles in its calculations. The AI does NOT replace any doctor at all. If you think you may be at risk for heart failure, go see a doctor. 

## Reflection
The process of this project when very smoothly. Although we ran into a couple issues. Firstly, buggs, we experienced lots of them. (more in detail explanation) 
Secondly, to improve the accuracy of the AI, we collected all the minimums and maximums of the variables in the dataset. At first it wasn't clear whether we should collect the minimums and maximums of the dataset, or the minimums and maximums in general.

## Citation
- scikit-learn (new BSD) https://pypi.org/project/scikit-learn/
- pandas (BSD 3-Clause License) https://github.com/pandas-dev/pandas/blob/master/LICENSE
- matplotlib (Python Software Foundation License (PSF)) https://pypi.org/project/matplotlib/3.4.3/
- numpy (BSD License (BSD)) https://github.com/numpy/numpy/blob/main/LICENSE.txt
- zeroone-ai (MIT) https://github.com/MathijsTak/ZeroOneAi
- PySimpleGUI (GNU Lesser General Public License v3.0) https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt
