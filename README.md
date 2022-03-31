# GitHub_Auto-Labeler


A tool for automatically labeling GitHub issues using BERT. The main model in this project was trained using the dataset provided in reference 1.

# Requirements

1. Install Docker
2. Install the docker image : https://hub.docker.com/repository/docker/kwedage/github_auto_labeler 
3. Install the model : https://drive.google.com/drive/folders/1_1lmUQevZ_OiZuPWVFRpggHATMKln2hn?usp=sharing
4. Install the datasets : https://www.kaggle.com/arbazkhan971/github-bugs-prediction-challenge-machine-hack

# Instructions

Once docker is installed. To run the GitHub Auto-Labeler all you need to run is the model_evaluating.py script.

`sudo docker run -v [DATASET PATH] -v [SCRIPTS PATH] --gpus all -it github_auto_labeler bash`
`python [SCRIPTS PATH]/model_evaluating.py`

The model_training.py script is intended to create the model file, if not downloaded. Adjustments can be made directly to the code of this file, to customize the model.

`sudo docker run -v [DATASET PATH] -v [SCRIPTS PATH] --gpus all -it github_auto_labeler bash`
`python [SCRIPTS PATH]/model_training.py`

The performance_comparison.py script is intended to compare the performance of the alternative implemention with the model.

`sudo docker run -v [DATASET PATH] -v [SCRIPTS PATH] --gpus all -it github_auto_labeler bash`
`python [SCRIPTS PATH]/performance_comparison.py`


# Files

The Scripts directory contains all the python scripts for this project. 

Model can be found at : 

## Scripts/model_training.py

This file is dedicated to determing the best parameters (hyperparameters) for the model used in this project.
In this project I explored various versions of BERT and various dropout values.

It is important to note that on line 9, 51 and 55 specific paths are used in order to refer to the original dataset, the location to save the models and the location to save the results. Please change these values to match your file structure. 

## Scripts/model_evaluating.py

This file is dedicated to evaluating a given model on a GitHub repository. Prior to running this file, a path to a saved model must be acquired, using the model_training.py file.   

## Scripts/performance_comparison.py

This file is intended to create GitHub issues and compare the performance of the saved model passed into it, with the alternative implementation found on GitHub marketplace, under larrylawl/Auto-Github-Issue-Labeller.

It is important to note that the alternative implementation was trained on a different training dataset and does not have entirely the same output classes (GitHub issue labels). 


# References:

- https://www.kaggle.com/arbazkhan971/github-bugs-prediction-challenge-machine-hack

- https://www.tensorflow.org/text/tutorials/classify_text_with_bert

- https://www.youtube.com/watch?v=D9yyt6BfgAM&ab_channel=codebasics
