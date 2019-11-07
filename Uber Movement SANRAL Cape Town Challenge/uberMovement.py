# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:23:17 2019

@author: devilears
"""



import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# I kept all the data files in this directory, so this needs to be pre-pended
data_dir = "data"


sample_sub = pd.read_csv(data_dir + "/SampleSubmission.csv")

# need to print it since this isn't a fancy jupyter notebook
#print(sample_sub.head())

data = pd.read_csv(data_dir + "/train.csv", 
                   parse_dates = ['Occurrence Local Date Time'])

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
#print(data[['longitude']])
#print(('latitude' in data.columns))
# These are both there.. but it can't find it... weird
# let's try deep magic

print(data.columns)
#data_cols = ["EventId", "Occurrence Local Date Time", "Reporting Agency", "Cause",
#             "Subcause", "Status", "longitude", "latitude", "road_segment_id"]
#data = data.reindex(columns=data_cols)

#data.columns = data.columns.to_series().apply(lambda x: x.strip())
#print(data.groupby('road_segment_id').mean())
    
# getting a KeyError: "['longitude'] not in index"
# despite the fact that it's there
# dafuq?
locations = data.groupby('road_segment_id').mean()[['longitude', 'latitude']]
locations.head(2)