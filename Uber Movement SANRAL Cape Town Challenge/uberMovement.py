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


# This is pointless, so I'm deleting them
#del data['Reporting Agency']
#del data['Status']

#print(('latitude' in data.columns))
#print(('longitude' in data.columns))

#print(data.colums)

# so far so good
#print(data.head())

# dafuq? I get 549, not 544 like the notebook
# this means that they removed the dodgy entries... there are exactly 5
# thanks for telling me, assholes
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
train.y.sum()


    
# $$$ Feature engineering $$$
train['datetime'] = pd.to_datetime(train['datetime'])
train['day'] = train['datetime'].dt.weekday_name

train['min'] = train['datetime'].dt.hour*60+train['datetime'].dt.minute
train.head()

# add locations to the segments
    
locations = data.groupby('road_segment_id').mean()[['longitude', 'latitude']]
locations.head(2)
# getting a KeyError: "['longitude'] not in index" -  this was due to dodgy entries

train = pd.merge(train, locations, left_on='segment_id', right_on='road_segment_id')
train.head()


# clean up old kak
data, local_test = 0,0



#$$$ Now the fun part CREATE THE MODEL! $$$
from catboost import CatBoostClassifier

#
#model = CatBoostClassifier(iterations=2,
#                           depth=2,
#                           learning_rate=0.03,
#                           loss_function='Logloss', 
#                           verbose=True) 
#
model = CatBoostClassifier(iterations=20, 
                           loss_function='Logloss', 
                           verbose=False) 

x_cols = ['day', 'segment_id', 'min', 'longitude', 'latitude']
cat_cols = ['day', 'segment_id']

model.fit(train[x_cols], train['y'], cat_features=cat_cols)




# $$$ Score the model $$$
from sklearn.metrics import log_loss

log_loss(train['y'], model.predict_proba(train[x_cols])[:, 1])

# Is this better than just 0s?
log_loss(train['y'], [0 for y in train['y']])

# Pre-process the test to match train
test['datetime'] = pd.to_datetime(test['datetime'])
test['day'] = test['datetime'].dt.weekday_name
test['min'] = test['datetime'].dt.hour*60+test['datetime'].dt.minute
test = pd.merge(test, locations, left_on='segment_id', right_on='road_segment_id')

# The important score
log_loss(test['y'], model.predict_proba(test[x_cols])[:, 1])

# First, just using .predict
from sklearn.metrics import f1_score
f1_score(test['y'], model.predict(test[x_cols]))

# Let's predict 1 even if the prob is just > 0.005
test['pred'] = model.predict_proba(test[x_cols])[:,1]
test['gt005'] = (test['pred']>0.005).astype(int)
#test.head()

f1_score(test['y'], test['gt005'])

# What about an even lower threshold?
test['gt0005'] = (test['pred']>0.0005).astype(int)
f1_score(test['y'], test['gt0005'])

# Hmm. And a higher 1?
test['gt05'] = (test['pred']>0.05).astype(int)
f1_score(test['y'], test['gt05'])