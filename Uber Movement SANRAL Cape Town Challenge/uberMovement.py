# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:23:17 2019

@author: devilears
"""



import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# I kept all the data files in this directory, so this needs to be pre-pended
# to any data file calls
data_dir = "data"


sample_sub = pd.read_csv(data_dir + "/SampleSubmission.csv")

# need to print it since this isn't a fancy jupyter notebook
#print(sample_sub.head())

data = pd.read_csv(data_dir + "/train.csv", 
                   parse_dates = ['Occurrence Local Date Time'])

# so far so good
# print(data.head())

# dafuq? I get 549, not 544 like the notebook
# perhaps they added missing data? 
data['road_segment_id'].unique().shape


# Training data from 2017
train = data.loc[data['Occurrence Local Date Time'] < '2018-01-01']
train = train.loc[train['Occurrence Local Date Time'] >= '2017-01-01']

# Testing data from 2018
local_test = data.loc[data['Occurrence Local Date Time'] < '2019-01-01']
local_test = local_test.loc[local_test['Occurrence Local Date Time'] >= '2018-09-01']

# $$$ Reshaping $$$
# Create a dataframe with a column for each segment_id (sid)
# Each row represents an hour.

sids = data['road_segment_id'].unique()

dts = pd.date_range('2017-01-01',
                    '2018-01-01',
                    freq="1h")
tr = pd.DataFrame({'datetime':dts})

for sid in sids:
    tr[str(sid)] = 0
    events = train.loc[train['road_segment_id'] == sid]
    dts = events['Occurrence Local Date Time'].dt.round('H')
    dates = dts.astype(str).unique()
    tr.loc[tr['datetime'].isin(dates), sid] = 1
tr.head()