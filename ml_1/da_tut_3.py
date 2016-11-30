#!/usr/bin/env python

import pandas as pd
import quandl

def main():
    '''
    This is the entry point of our application
    '''

    ## Setup some basic variables
    api_key    = open('quandl_key.txt', 'r').read().rstrip()
    states_url = 'https://simple.wikipedia.org/wiki/List_of_U.S._states'

    ## Configure quandl
    quandl.ApiConfig.api_key = api_key

    ## Read our data from wikipedia
    states = pd.read_html(states_url)

    df = pd.DataFrame()

    for abbr in states[0][0][1:]:
        abbr = str(abbr)
        key = 'FMAC/HPI_%s' % abbr
        df_hpi  = quandl.get(key)

        ## The joinin was all extra stuff that I did
        df_hpi.rename(columns={'Value': abbr}, inplace=True)
        df = df.join(df_hpi, how='outer')

    print(df.tail())

if (__name__ == '__main__'):
    main()
