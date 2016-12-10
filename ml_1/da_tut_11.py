#!/usr/bin/env python

## This script covers various rolling statistics
## https://pythonprogramming.net/rolling-statistics-data-analysis-python-pandas-tutorial/

import pandas as pd
from pathlib import Path
import quandl as ql
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

def main():
    '''
    Main entry point
    '''
    api_key = open('quandl_key.txt').read().rstrip()
    ql.ApiConfig.api_key = api_key

    df = get_state_data()

    ## Get a 12 month moving average for Texas
    df['TX_12MA'] = df['TX'].rolling(12).mean()
    ## Get the 12 month stdv
    df['TX_12STD'] = df['TX'].rolling(12).std()
    ## NaN will be generated w/ rolling operations because @ the start
    ## there is not enough data to calculate
    df.dropna(inplace=True)


    ## Plot the 12 M/A for TX
    #tx_df.plot()
    #plt.legend().remove()
    #plt.savefig('charts/tut_11_tx.pdf', format='pdf')

    fig = plt.figure()
    ax1 = plt.subplot2grid((2,1), (0,0))
    ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

    # df['TX'].plot(ax=ax1)
    # df['TX_12MA'].plot(ax=ax1)
    # df['TX_12STD'].plot(ax=ax2)
    #
    # plt.legend().remove()
    # plt.savefig('charts/tut_11_std.pdf', format='pdf')

    ## Get moving correlation w/ TX & AK
    TX_AK_12corr = df['AK'].rolling(12).corr(df['TX'])

    df['TX'].plot(ax=ax1, label='TX HPI')
    df['AK'].plot(ax=ax1, label='AK HPI')
    TX_AK_12corr.plot(ax=ax2)

    ## Put the legend @ the bottom right hand corner
    ax1.legend(loc=4)

    plt.savefig('charts/tut_11_corr.pdf', format='pdf')

def fiddy_states():
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def get_state_data():
    p_file = Path('pickles/tut_11.pickle')
    if p_file.is_file():
        print('Loading from pickle')
        main_df = pd.read_pickle(str(p_file))
    else:
        print('Loading data from wikipedia')
        main_df = pd.DataFrame()
        for abbr in fiddy_states():
            print(abbr)
            df = ql.get('FMAC/HPI_' + abbr)
            k  = 'Value'
            df.rename(columns={k: abbr}, inplace=True)
            df[abbr] = (df[abbr] - df[abbr][0]) / df[abbr][0] * 100.0

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        print('Saving pickle file')
        main_df.to_pickle(str(p_file))

    return main_df


if __name__ == '__main__':
    main()
