#!/usr/bin/env python

## Joining 30yr mortgage rate
## https://pythonprogramming.net/joining-mortgage-rate-data-analysis-python-pandas-tutorial/

import pandas as pd
import quandl as ql
from pathlib import Path
import pickle

def main():
    '''
    Main entry point
    '''
    ql.ApiConfig.api_key = open('quandl_key.txt', 'r').read().rstrip()
    m_rate = mortgage_30y()
    df = HPI_states()
    bm = HPI_benchmark()

    state_hpi_30m = df.join(m_rate)
    print(state_hpi_30m.corr()['M30'].describe())


def mortgage_30y():
    '''
    Get 30 yr conventional mortgage rate
    '''
    df = ql.get('FMAC/MORTG', start_date='1975-01-01')
    ## Get the perc change
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100
    df = df.resample('D').ffill().resample('M').mean()
    df.columns = ['M30']
    return df

def fiddy_states():
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def HPI_states():
    pckl_file = Path('pickles/tut_13.pickle')
    if (pckl_file.is_file()):
        print('Reading from pickle')
        main_df = pd.read_pickle(str(pckl_file))
    else:
        print('Reading from wikipedia')
        main_df = pd.DataFrame()
        for abbr in fiddy_states():
            print(abbr)
            df = ql.get('FMAC/HPI_' + abbr)
            df.columns = [abbr]
            df[abbr] = (df[abbr] - df[abbr][0]) / df[abbr][0] * 100.00

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        ## Save file
        print('Saving pickle')
        p_file = open(str(pckl_file), 'wb')
        pickle.dump(main_df, p_file)
        p_file.close()

    return main_df

def HPI_benchmark():
    df = ql.get('FMAC/HPI_USA')
    df.columns = ['USA']
    df['USA'] = (df['USA'] - df['USA'][0]) / df['USA'][0] * 100
    return df

if __name__ == '__main__':
    main()
