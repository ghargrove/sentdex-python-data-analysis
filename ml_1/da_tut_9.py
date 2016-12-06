#!/usr/bin/env python

import pandas as pd
import quandl as ql
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('fivethirtyeight')

def main():
    '''
    Main entry point
    '''

    ## Setup quandl
    api_key = open('quandl_key.txt', 'r').read().rstrip()
    ql.ApiConfig.api_key = api_key

    ## Grab our data
    df = HPI_by_state()
    TX1yr = df['TX'].resample('A').mean()
    print(TX1yr.head())

    ## Create our figure
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))

    ## Plot data
    df['TX'].plot(ax=ax1)
    TX1yr.plot(ax=ax1, color='k')

    plt.legend().remove()
    plt.savefig('charts/tut_9.pdf', format='pdf')

def fiddy_states():
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def HPI_benchmark():
    k = 'Value'
    df = ql.get('FMAC/HPI_USA')
    df[k] = (df[k] - df[k][0]) / df[k][0] * 100.0
    df.rename(columns={k: 'US'}, inplace=True)
    return df

def HPI_by_state():

    ## Load from a pickle if possible
    pp = Path('pickles/tut_9.pickle')

    if pp.is_file():
        main_df = pd.read_pickle(pp.name)
    else:
        main_df = pd.DataFrame()

        for abbr in fiddy_states():
            k = 'Value'
            df = ql.get('FMAC/HPI_' + abbr)
            df[k] = (df[k] - df[k][0]) / df[k][0] * 100.0
            df.rename(columns={'Value': abbr}, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        ## Pickle the df
        pf = open(pp.name, 'wb')
        pickle.dump(main_df, pf)
        pf.close()

    return main_df

if __name__ == '__main__':
    main()
