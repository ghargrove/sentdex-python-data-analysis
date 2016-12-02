#!/usr/bin/env python
'''
This script is for data analysis tutorial 8
https://pythonprogramming.net/percent-change-correlation-data-analysis-python-pandas-tutorial/
'''
import pickle
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import quandl as ql

style.use('fivethirtyeight')

api_key = open('quandl_key.txt', 'r').read().rstrip()

def get_states():
    '''
    Get a list of states
    '''
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def grab_initial_state_data():

    p_file  = Path('fiddy_states3.pickle')

    ## If we have a pickle file just use that data
    if p_file.is_file():
        print('Loading dataset from a pickle')
        main_df = pd.read_pickle(p_file.name)
    else:
        print('Building dataset')
        main_df = pd.DataFrame()
        for abbr in get_states():
            query = 'FMAC/HPI_' + str(abbr)
            df = ql.get(query, authtoken=api_key)
            ## We need to rename the col
            df.rename(columns={'Value': str(abbr)}, inplace=True)

            ## This performs a rolling percentage change
            # df = df.pct_change()

            ## Calculate the percentage change from the beginning
            df[abbr] = (df[abbr] - df[abbr][0]) / df[abbr][0] * 100.0

            print(query)
            print(df.tail())

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        ## Pickle the data frame so we don't have to load it again
        ## Do it the long way using the pickle module
        pickle_file = open(p_file.name, 'wb')
        pickle.dump(main_df, pickle_file)
        pickle_file.close()

    return main_df

def hpi_benchmark():
    '''
    Get a benchmark
    '''

    df = ql.get('FMAC/HPI_USA', authtoken=api_key)
    df.rename(columns={'Value': 'United States'}, inplace=True)
    df['United States'] = (df['United States'] - df['United States'][0]) / df['United States'][0] * 100.0
    return df


def main():
    '''
    This is the applications main entry point
    '''

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    HPI_data  = grab_initial_state_data()
    HPI_state_correlation = HPI_data.corr()
    benchmark = hpi_benchmark()

    print(HPI_state_correlation)
    print(HPI_state_correlation.describe())

    ## Plot this fuckin data
    HPI_data.plot(ax=ax1, linewidth=1)
    benchmark.plot(color='k', ax=ax1, linewidth=10)

    plt.legend().remove()
    plt.savefig('charts/HPI_data4.pdf', format='pdf')


if __name__ == '__main__':
    main()
