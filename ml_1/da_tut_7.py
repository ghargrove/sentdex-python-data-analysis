#!/usr/bin/env python

## This tut covers pickling
## https://pythonprogramming.net/pickle-data-analysis-python-pandas-tutorial/

import pandas as pd
import quandl as ql
import pickle

def main():
    '''
    This is the main entry point for our script
    '''
    print('Learning about pickling!!!')
    grab_initial_state_data()

def state_list():
    '''
    Returns a list of the 50 US state abbreviations
    '''
    states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return states[0][0][1:]

def grab_initial_state_data():

    api_key = open('quandl_key.txt', 'r').read().rstrip()
    main_df = pd.DataFrame()
    ## Loop through the states
    for abbr in state_list():
        query = 'FMAC/HPI_' + str(abbr)
        df = ql.get(query, authtoken=api_key)
        df.rename(columns={'Value': str(abbr)}, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    ## Pickle this mutha fucka

    pickle_out = open('fiddy_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


if __name__ == '__main__':
    main()
