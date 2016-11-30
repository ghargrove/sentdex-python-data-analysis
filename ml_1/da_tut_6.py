#!/usr/bin/env python

import pandas as pd

df_1 = pd.DataFrame({
    'HPI':              [80, 85, 88, 85],
    'Int_rate':         [2,  3,  2,  2],
    'US_GDP_Thousands': [50, 55, 65, 55]
}, index=[2001, 2002, 2003, 2004])

df_2 = pd.DataFrame({
    'HPI':              [80, 85, 88, 85],
    'Int_rate':         [2,  3,  2,  2],
    'US_GDP_Thousands': [50, 55, 65, 55]
}, index=[2005, 2006, 2007, 2008])

df_3 = pd.DataFrame({
    'HPI':          [80, 85, 88, 85],
    'Unemployment': [7,  8,  9,  6],
    'Low_tier_HPI': [50, 52, 50, 53]
}, index=[2001, 2002, 2003, 2004])

df_1.set_index('HPI', inplace=True)
df_3.set_index('HPI', inplace=True)

df_4 = df_1.join(df_3)
# print(df_4)


df_1 = pd.DataFrame({
    'Int_rate': [2, 3, 2, 2],
    'US_GDP_Thousands': [50, 55, 65, 55],
    'Year': [2001, 2002, 2003, 2004]
})

df_3 = pd.DataFrame({
    'Unemployment': [7, 8, 9, 6],
    'Low_tier_HPI': [50, 52, 50, 53],
    'Year': [2001, 2003, 2004, 2005]
})

## Merge our DataFrames that are missing dates
df_m = pd.merge(df_1, df_3, on="Year", how="outer")
df_m.set_index('Year', inplace=True)
print(df_m)

## Next check out joining
df_1.set_index('Year', inplace=True)
df_3.set_index('Year', inplace=True)

print(df_1.join(df_3, how="outer"))
