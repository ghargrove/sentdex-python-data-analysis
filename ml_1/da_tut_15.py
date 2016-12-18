#!/usr/bin/env python

## This tutorial covers mapping functions.
## Its going to pickup from tut 14
## https://pythonprogramming.net/rolling-apply-mapping-functions-data-analysis-python-pandas-tutorial/

from pathlib import Path
import quandl as ql
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean

style.use('fivethirtyeight')

def create_labels(curr_hpi, fut_hpi):
    ''' Indicates if the price has gone up '''
    if fut_hpi > curr_hpi:
        return 1
    else:
        return 0

def moving_averages(values):
    ''' Calculate the average of a bunch of values '''
    ma = mean(values)
    return ma

def main():
    hpi_pickle = Path('pickles/HPI.pickle')
    if hpi_pickle.is_file():

        print('Loading HPI data from pickle')
        housing_data = pd.read_pickle(str(hpi_pickle))
        ## Get the pct change
        housing_data = housing_data.pct_change()
        ## Remove inf values
        housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        ## Add a future column
        housing_data['HPI_US_Future'] = housing_data['HPI_US'].shift(-1)
        housing_data.dropna(inplace=True)

        housing_data['label'] = list(
            map(create_labels, housing_data['HPI_US'], housing_data['HPI_US_Future'])
        )

        ## Perform a rolling apply
        housing_data['ma_apply_example'] = housing_data['30M'].rolling(10).apply(moving_averages)
        print(housing_data.tail())


        ## Do some weird replace thing
        # housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        # housing_data['US_HPI_future'] = housing_data['HPI_US'].shift(-1)
        #
        # housing_data.dropna(inplace=True)
        #
        # print(housing_data.tail())


    else:
        print('Could not load HPI data')

if __name__ == '__main__':
    main()
