from github3 import login
from getpass import getpass
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_text

def gitHubLogin():
    print('Please enter your Github credentials')
    for i in range(3):
        try:
            username = input('GitHub username: ')
            password = getpass()
            repository = input('GitHub repository: ') # Example: GitHub_Auto-Labeler
            gh = login(username, password)
            repo = gh.repository(username, repository)
            return gh, username, repo
        except:
            print('Username and password combination is incorrect.')

def pushIssuesToRepo(repo):
    # Get local issues from dataset
    ds_path = 'var/DataSets/664/test.json'
    df = pd.read_json(ds_path)
    numberOfTests = min(30000, int(input('Please enter the number of issues to test (max = 30000): ')))

    for i in range(0, numberOfTests):
        repo.create_issue(title=df['title'][i], body=df['body'][i])

    print(f'Successfully pushed {numberOfTests} issues to {repo.name}')

def alternativeLabelIntoInteger(label):
    return ['bug', 'enhancement', 'question', 'doc'].index(label)

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

        print(labels)

def getModel():  
    while(1):
        try:
            model_path = input('Please enter the saved model\'s path: ')
            if(model_path.strip().lower() == 'exit'):
                break
            model = tf.keras.models.load_model('/var/Scripts/664/Models/0') # Example: /var/Scripts/664/Models/0
            print('Successfully found model.')
            return model
        except Exception as e:
            print('There was an error with the path specified.\n Make sure the path is to the entire folder for the model.')
            print(e)

def getTestDS():
    while(1):
        try:
            ds_path = input('Please enter the test dataset\'s path: ')
            if(ds_path.strip().lower() == 'exit'):
                break
            ds = pd.read_json('var/DataSets/664/test.json') #Example: 'var/DataSets/664/test.json'
            print('Successfully found expected json dataset.')
            return ds
        except Exception as e:
            print('There was an error with the path specified or the expected format of the dataset (json). \n')
            print(e)


def evaluateLocalModel():
    ds = getTestDS()
    model = getModel()
    temp_output = model.predict(ds[['title','body']].agg('. '.join, axis=1))
    output = tf.nn.softmax(temp_output)
    prediction = np.argmax(output, axis=1)

    print(prediction)
def main():
    gh, username, repo = gitHubLogin()
    #evaluateLocalModel()
    pushIssuesToRepo(repo)
    evaluateAlternativeMethod(repo)
if __name__ == '__main__':
    main()
