# GitHub_Auto-Labeler


A tool for automatically labeling GitHub issues using BERT. The main model in this project was trained using the dataset provided in reference 1. Altogether, this project was a great opportunity to learn about Natural Language Processing (BERT) and to apply these concepts to a practical application (GitHub issue labeling). 

# Requirements

1. Install Docker
2. Install the docker image : https://hub.docker.com/repository/docker/kwedage/github_auto_labeler 
3. Install the model : https://drive.google.com/drive/folders/1_1lmUQevZ_OiZuPWVFRpggHATMKln2hn?usp=sharing
4. Install the datasets : https://www.kaggle.com/arbazkhan971/github-bugs-prediction-challenge-machine-hack

Note save the model to the datasets directory, unless you wish to mount an additional volume to the docker image.

# Instructions

Once docker is installed. To run the GitHub Auto-Labeler all you need to run is the model_evaluating.py script. The  `-v [DATASET PATH]` is unneccessary if you do not plan on running the model_training.py or perfomance_comparison.py files. The `--gpus all` option may or may not work on your system without installing nvidia/cuda. Installation guide can be found here: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html. You can attempt to run the files without it, but all my testing was done with it. A demo of running the the main tool (model_evaluation) can be found here: https://drive.google.com/file/d/1ZgzX4ExcRs9II0P7gQm0Y9mr8ixnIczu/view?usp=sharing. 

```bash
sudo docker run -v [DATASET PATH]:[MOUNTED DATASET PATH] -v [SCRIPTS PATH]:[MOUNTED SCRIPT PATH] --gpus all -it github_auto_labeler bash
python [SCRIPTS PATH]/model_evaluating.py
```

The model_training.py script is intended to create the model file, if not downloaded. Adjustments can be made directly to the code of this file, to customize the model.

```bash
sudo docker run -v [DATASET PATH]:[MOUNTED DATASET PATH] -v [SCRIPTS PATH]:[MOUNTED SCRIPT PATH]  --gpus all -it github_auto_labeler bash
python [SCRIPTS PATH]/model_training.py
```

The performance_comparison.py script is intended to compare the performance of the alternative implemention with the model. IMPORTANT: This file should be edited to run the desired functionality. Currently it is set to close all open issues. Just comment/uncomment the desired functions in the main method. 

```bash
sudo docker run -v [DATASET PATH]:[MOUNTED DATASET PATH] -v [SCRIPTS PATH]:[MOUNTED SCRIPT PATH]  --gpus all -it github_auto_labeler bash
python [SCRIPTS PATH]/performance_comparison.py
```

# Files

The Scripts directory contains all the python scripts for this project. 

## Scripts/model_training.py

This file is dedicated to determing the best parameters (hyperparameters) for the model used in this project.
In this project I explored various versions of BERT and various dropout values.

It is important to note that on line 9, 51 and 55 specific paths are used in order to refer to the original dataset, the location to save the models and the location to save the results. Please change these values to match your file structure. 

## Scripts/model_evaluating.py

This file is dedicated to evaluating a given model on a GitHub repository. Prior to running this file, a path to a saved model must be acquired, using the model_training.py file.   

## Scripts/performance_comparison.py

This file is intended to create GitHub issues and compare the performance of the saved model passed into it, with the alternative implementation found on GitHub marketplace, under larrylawl/Auto-Github-Issue-Labeller.

However, some issues came up when trying to compare the performance of this tool and the alternative implemention by Larry Lawl, this includes: a limitation in the amount of issues that the GitHub API allows to push in one session, the time it takes for the GitHub action to run (greater than 1 minute per issue), and the classes of labels that each model outputs (Bug, Feature, Question vs. Bug, Enchancement, Documentation). Not to mention, a standard test dataset that both models can fairly compare against. 


# References:

- https://www.kaggle.com/arbazkhan971/github-bugs-prediction-challenge-machine-hack

- https://www.tensorflow.org/text/tutorials/classify_text_with_bert

- https://www.youtube.com/watch?v=D9yyt6BfgAM&ab_channel=codebasics
