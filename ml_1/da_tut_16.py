#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn import svm, preprocessing, model_selection
import sklearn as skl

## svm = Support Vector Machine
## We will use the svm library for our machine learning classifier

## Preprocessing is used to adjust our dataset
## Typically ML will be a bit more accurate if your features are between 1 & -1

## cross_validation is a library that we'll be using to create our training and
## testing sets

def create_label(curr_hpi, fut_hpi):
    if fut_hpi > curr_hpi:
        return 1
    else:
        return 0

def get_data():
    pickle_file = Path('pickles/HPI.pickle')
    if pickle_file.is_file():
        df = pd.read_pickle(str(pickle_file))

        df = df.pct_change()
        df.replace([-np.inf, np.inf], np.nan, inplace=True)
        df['HPI_US_future'] = df['HPI_US'].shift(-1)
        df.dropna(inplace=True)
        df['label'] = list(map(create_label, df['HPI_US'], df['HPI_US_future']))
    else:
        print('Could not load pickle file')

    return df

def main():

    ## Get our data
    df = get_data()

    ## Create our featureset
    X = np.array(df.drop(['label', 'HPI_US_future'], 1))
    X = preprocessing.scale(X)

    ## Create our label
    y = np.array(df['label'])


    ## Split up our data into training and testing subsets
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

    ## Establish the classifier that we want to use
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    print(clf.score(X_test, y_test))

if __name__ == '__main__':
    main()
