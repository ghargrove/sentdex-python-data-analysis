#!/usr/bin/env python

## Just joining more data
## https://pythonprogramming.net/economic-factors-data-analysis-python-pandas-tutorial/

import pandas as pd
import quandl as ql
from pathlib import Path

def main():
    ql.ApiConfig.api_key = open('quandl_key.txt', 'r').read().rstrip()

    ## Get our data
    HPI_data = states_HPI()
    m30 = mortgage_30y()
    sp500 = sp500_data()
    gdp = gdp_data()
    HPI_bench = benchmark_HPI()
    unemployment = us_unemployment()

    HPI = HPI_data.join([HPI_bench, m30, sp500, gdp, unemployment])
    HPI.dropna(inplace=True)

    ## Print correlation
    # print(HPI.corr())

    ## This is used in the next tut
    HPI.to_pickle('pickles/HPI.pickle')


def fiddy_states():
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def states_HPI():
    '''
    Get HPI for each state
    '''
    pckl = Path('pickles/tut_14.pickle')
    if pckl.is_file():
        print('Loading from archive')
        main_df = pd.read_pickle(str(pckl))
    else:
        print('Loading from wikipedia')
        main_df = pd.DataFrame()
        for abbr in fiddy_states():
            print(abbr)
            df = ql.get('FMAC/HPI_' + abbr)
            df.rename(columns={'Value': abbr}, inplace=True)
            df[abbr] = (df[abbr] - df[abbr][0]) / df[abbr][0] * 100

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df)

        main_df.to_pickle(str(pckl))
    return main_df

def benchmark_HPI():
    '''
    Get HPI data for the US
    '''
    print('Getting benchmark')
    df = ql.get('FMAC/HPI_USA')
    df.rename(columns={'Value': 'HPI_US'}, inplace=True)
    df['HPI_US'] = (df['HPI_US'] - df['HPI_US'][0]) / df['HPI_US'][0] * 100.0
    return df

def mortgage_30y():
    '''
    Economic indicator: 30year mortgage rate
    '''
    print('Getting 30yr M')
    df = ql.get('FMAC/MORTG')
    df.rename(columns={'Value': '30M'}, inplace=True)
    df['30M'] = (df['30M'] - df['30M'][0]) / df['30M'][0] * 100.0
    df = df.resample('1D').mean()
    df = df.resample('M').mean()
    return df

def sp500_data():
    print('Getting SP500')
    df = ql.get('YAHOO/INDEX_GSPC', start_date='1975-01-01')
    k = 'Adjusted Close'
    df[k] = (df[k] - df[k][0]) / df[k][0] * 100.0
    df = df.resample('M').mean()
    df.rename(columns={k: 'sp500'}, inplace=True)
    return df['sp500']

def gdp_data():
    '''
    Economic indicator: GDP (Gross Domestic Product)
    '''
    print('Getting GDP')
    df = ql.get('BCB/4385', start_date='1975-01-01')
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    df.rename(columns={'Value': 'GDP'}, inplace=True)
    df = df.resample('M').mean()
    return df['GDP']

def us_unemployment():
    '''
    Economic indicator: US unemployment data
    '''
    print('Getting unemployment')
    df = ql.get('ECPI/JOB_G', start_date='1975-01-01')
    k = 'Unemployment Rate'
    df[k] = (df[k] - df[k][0]) / df[k][0] * 100.0
    df = df.resample('1D').mean()
    df = df.resample('M').mean()
    return df



if __name__ == '__main__':
    main()
