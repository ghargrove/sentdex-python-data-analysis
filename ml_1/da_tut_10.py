#!/usr/bin/env python

## This tutorial covers handling missing data
## https://pythonprogramming.net/nan-na-missing-data-analysis-python-pandas-tutorial/

import pandas as pd
import quandl as ql
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

def main():
    '''
    Application entry point
    '''
    ## Configure Quandl
    api_key = open('quandl_key.txt', 'r').read().rstrip()
    ql.ApiConfig.api_key = api_key

    ## Grab data & resample
    df  = get_state_data()

    df['TX1yr'] = df['TX'].resample('A').mean()



    # df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    # Fill the NaN w/ a value. Could be useful for machin learning
    # df.fillna(value=-99999, inplace=True) 

    df.dropna(inplace=True)
    # df.dropna(how='all', inplace=True) - Remove only if all cols are NaN

    print(df[['TX', 'TX1yr']])

    ## Graph it
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    df['TX'].plot(ax=ax1)
    df['TX1yr'].plot(color='k', ax=ax1)

    plt.legend().remove()
    plt.savefig('charts/tut_10_bfill.pdf', format='pdf')

def fiddy_states():
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def get_state_data():
    '''
    Load state data from Quandl using wikipedia for states
    '''
    p_file  = Path('pickles/state_data.pickle')
    if p_file.is_file():
        print('Build dataframe from pickle')
        main_df = pd.read_pickle(str(p_file))
    else:
        print('Pulling data...')
        main_df = pd.DataFrame()
        for abbr in fiddy_states():
            print(abbr)
            col = 'Value'
            df  = ql.get('FMAC/HPI_' + abbr)
            ## Get the % change from the start
            df[col] = (df[col] - df[col][0]) / df[col][0] * 100
            ## Rename the column after the state
            df.rename(columns={col: abbr}, inplace=True)

            ## Append the data to our set of states
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        ## Save pickle data
        print('Creating pickle file')
        pckl = open(str(p_file), 'wb')
        pickle.dump(main_df, pckl)
        pckl.close()

    return main_df


if __name__ == '__main__':
    main()
