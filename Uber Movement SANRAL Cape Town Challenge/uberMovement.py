# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:23:17 2019

@author: devilears
"""



import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

sample_sub = pd.read_csv('data/SampleSubmission.csv')

data = pd.read_csv('data/train.csv', 
                   parse_dates = ['Occurrence Local Date Time'])

#There are null values for the reporting agency. Not sure how this is relevant
#TODO Can also drop Status since it adds nothing
data['Reporting Agency'].fillna('Camera', inplace=True)
#print(data.isnull().any())

#print(('latitude' in data.columns))
#print(('longitude' in data.columns))
#print(data['longitude'])
#print(data['latitude'])
#print(data['road_segment_id'])

#print(data.colums)

# so far so good
# print(data.head())

# dafuq? I get 549, not 544 like the notebook
# perhaps they added missing data? # to any data file calls

#print(data['road_segment_id'].unique().shape)


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

# Reshape this as in sample submission
# I add some extra columns that may be useful
train = pd.DataFrame({
    'datetime x segment_id':np.concatenate([[str(x) + " x " + str(c) 
                                             for c in sids] 
                                            for x in tr['datetime']]),
    'datetime':np.concatenate([[str(x) for c in sids] for x in tr['datetime']]),
    'segment_id':np.concatenate([[str(c) for c in sids] for x in tr['datetime']]),
    'y':tr[sids].values.flatten()
})
train.head()


# Same for local test
dts = pd.date_range('2018-09-01','2018-12-31',
                    freq="1h")
tr = pd.DataFrame({'datetime':dts})

for sid in sids:
    tr[str(sid)] = 0
    events = local_test.loc[local_test['road_segment_id'] == sid]
    dts = events['Occurrence Local Date Time'].dt.round('H')
    dates = dts.astype(str).unique()
    tr.loc[tr['datetime'].isin(dates), sid] = 1
    
test = pd.DataFrame({
    'datetime x segment_id':np.concatenate([[str(x) + " x " + str(c) 
                                             for c in sids] 
                                            for x in tr['datetime']]),
    'datetime':np.concatenate([[str(x) for c in sids] for x in tr['datetime']]),
    'segment_id':np.concatenate([[str(c) for c in sids] for x in tr['datetime']]),
    'y':tr[sids].values.flatten()
})
test.head()
# I get 14 234, whereas the notebook gets 14 235. Once fewer accident I suppose?
train.y.sum()


    
# $$$ Feature engineering $$$
train['datetime'] = pd.to_datetime(train['datetime'])
train['day'] = train['datetime'].dt.weekday_name

train['min'] = train['datetime'].dt.hour*60+train['datetime'].dt.minute
train.head()

# add locations to the segments
    
#locations = data.groupby('road_segment_id').mean()[['longitude', 'latitude']]
#locations.head(2)
# getting a KeyError: "['longitude'] not in index"
# despite the fact that it's there
# dafuq?
# fuck knows but this fixes it. no mean, though
locations = data[['road_segment_id','longitude','latitude']]
locations.head(2)

# clean up old kak
data, local_test = 0,0

#print(train.shape)
train = train[:locations.shape[0]]
#print(locations.shape[0])

# Keep running out of memory.. shyte

train = pd.merge(train, locations, left_on='segment_id', right_on='road_segment_id')
train.head()
