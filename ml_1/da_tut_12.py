#!/usr/bin/env python

## This script covers applying comparison operators to Pandas Dataframes
## https://pythonprogramming.net/comparison-operators-data-analysis-python-pandas-tutorial/

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

def main():
    '''
    Main entry point
    '''
    bridge_height = {'meters': [10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}
    df = pd.DataFrame(bridge_height)

    df['std'] = df['meters'].rolling(window=2).std()

    print(df)

    df_std = df.describe()['meters']['std']
    ## Logically modify the dataframe. This will return a Dataframe of booleans
    mask = df['std'] < df_std
    df = df[mask]

    print(df)


    ## Plot the measurements
    df['meters'].plot()
    plt.savefig('charts/tut_12_heights.pdf', format='pdf')

if __name__ == '__main__':
    main()
