import time
from xml.etree.ElementPath import prepare_descendant
from github3 import login
from getpass import getpass
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_text



def gitHubLoginAndReturnRepo():
    print('Please enter your Github credentials')
    for i in range(3):
        try:
            username = input('GitHub username: ')
            password = getpass()
            gh = login(username, password)
            repository = input('GitHub repository: ') # Example: GitHub_Auto-Labeler_v2
            repo = gh.repository(username, repository)
            return repo
        except:
            print('Username and password combination is incorrect.')

def pushIssuesToRepoFromDataset(repo):
    # Get local issues from dataset
    ds_path = 'var/DataSets/664/train_extra.json'
    df = pd.read_json(ds_path)
    numberOfTests = min(20, int(input('Please enter the number of issues to push (max ~ 20): ')))

    for i in range(0, numberOfTests):
        repo.create_issue(title=df['title'][i], body=df['body'][i])

    print(f'Successfully pushed {numberOfTests} issues to {repo.name}')

def alternativeLabelIntoInteger(label):
    return ['bug', 'enhancement', 'question', 'doc'].index(label)

def closeAllOpenIssues(repo):
    repo = repo.refresh()
    issues = repo.issues()

    for issue in issues:
        if (issue.is_closed()):
            continue
        else:
            issue.close()

def evaluateAlternativeMethod(repo):
    print('Assumptions: \n'
        '\t- There is no open issues other than the ones created from pushIssuesToRepo()\n'
        '\t- The alternative tool has run, and has labeled each of the issues.\n')
    c = input('Are the assumptions correct (Y|N): ').strip().lower()
    if(c == 'y' or c == 'yes'):
        repo = repo.refresh()
        issues = repo.issues()

        labels = []
        for issue in issues:
            if (issue.is_closed()):
                continue
            for issue_label in issue.labels():
                labels.append(alternativeLabelIntoInteger(issue_label.name))

        ds = getTestDS(10) # The number of data entries to test
        getPerformance(ds, labels)

def getModel():  
    while(1):
        try:
            model_path = input('Please enter the saved model\'s path: ')
            if(model_path.strip().lower() == 'exit'):
                break
            model = tf.keras.models.load_model(model_path) # Example: /var/Scripts/664/Models/0
            print('Successfully found model.')
            return model
        except Exception as e:
            print('There was an error with the path specified.\n Make sure the path is to the entire folder for the model.')
            print(e)

def getTestDS(maxRows):
    while(1):
        try:
            ds_path = input('Please enter the test dataset\'s path: ')
            if(ds_path.strip().lower() == 'exit'):
                break
            ds = pd.read_json(ds_path) #Example: 'var/DataSets/664/train_extra.json'
            print('Successfully found expected json dataset.')
            return ds.iloc[:min(maxRows, len(ds))]
        except Exception as e:
            print('There was an error with the path specified or the expected format of the dataset (json). \n')
            print(e)

def getPerformance(ds, prediction, three_class_test = False):
    class_count = [0, 0, 0]
    true_positives = [0, 0, 0]

    for i in range(min(len(ds), len(prediction))):
        actual = int(ds.iloc[i][2])
        class_count[actual] += 1
        if(prediction[i] == actual):
            true_positives[actual] += 1

    print(f'2-class overall accuracy: {(true_positives[0] + true_positives[1])/(class_count[0] + class_count[1])}')
    if(three_class_test):
        print(f'3-class overall accuracy: {np.sum(true_positives)/np.sum(class_count)}')

def evaluateLocalModel():
    ds = getTestDS(min(int(input('Enter the number of data rows to test (max 300000): ')), 300000))
    model = getModel()
    print('Predicting...')
    temp_output = model.predict(ds[['title','body']].agg('. '.join, axis=1))
    output = tf.nn.softmax(temp_output)
    prediction = np.argmax(output, axis=1)
    print('Obtained predictions')
    getPerformance(ds, prediction, True)


# Uncomment the commands to run
def main():
    repo = gitHubLoginAndReturnRepo()
    evaluateLocalModel()
    #pushIssuesToRepoFromDataset(repo)
    #evaluateAlternativeMethod(repo)
    #closeAllOpenIssues(repo)

if __name__ == '__main__':
    main()
