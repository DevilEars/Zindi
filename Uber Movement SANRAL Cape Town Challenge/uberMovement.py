# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:23:17 2019

@author: devilears
"""



import pandas as pd
import numpy as np
#from matplotlib import pyplot as plt

sample_sub = pd.read_csv('data/SampleSubmission.csv')

data = pd.read_csv('data/train.csv', 
                   parse_dates = ['Occurrence Local Date Time'])


# This is pointless, so I'm deleting them
#del data['Reporting Agency']
#del data['Status']

# dafuq? I get 549, not 544 like the notebook
# this means that they removed the dodgy entries... there are exactly 5
# thanks for telling me, assholes
data['road_segment_id'].unique().shape


# Training data from 2017
# Remember to train on all the data
#train = data.loc[data['Occurrence Local Date Time'] < '2018-01-01']
#train = train.loc[train['Occurrence Local Date Time'] >= '2017-01-01']

train = data.loc[data['Occurrence Local Date Time'] < '2018-01-01']
train = train.loc[train['Occurrence Local Date Time'] >= '1930-01-16']

train = data.loc[data['Occurrence Local Date Time']]

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


# clean up
data, local_test = 0,0



#$$$ Now the fun part CREATE THE MODEL! $$$
from catboost import CatBoostClassifier

model = CatBoostClassifier(iterations=23,
                           depth=6,
                           learning_rate=0.03,
                           loss_function='Logloss', 
                           verbose=False) 

x_cols = ['day', 'segment_id', 'min', 'longitude', 'latitude']
cat_cols = ['day', 'segment_id']

model.fit(train[x_cols], train['y'], cat_features=cat_cols)


# $$$ Score the model $$$
from sklearn.metrics import log_loss
from sklearn.metrics import f1_score

'''
$$$ Score the model $$$
1. make predictions from themodel
2. check if it's better than just 0s
3. pre-process test data to match training data
4. check log loss score
5. check f1 score of predictions
6. check what different thresholds do to f1 score
'''
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

f1_score(test['y'], model.predict(test[x_cols]))

# Let's predict 1 even if the prob is just > 0.005
test['pred'] = model.predict_proba(test[x_cols])[:,1]

test['gt0m'] = (test['pred']> test['pred'].mean()).astype(int)
f1_score(test['y'], test['gt0m']) # 0.0014542921105262002

# need to beat 0.014560843 - DONE
# need to beat 0.04

def make_submission():
    '''
    $$$ Making a submission $$$
    1. Make the data frame from the sample submisison file
    2. Add extra features
    3. Make predictions
    4. Apply the threshold for predictions
    5. Save to csv for submission
    '''
     
    # Make the dataframe - dates based on sample submission file
    dts = pd.date_range('2019-01-01 01:00:00',
                        '2019-03-31 23:00:00',
                        freq="1h")
    tr = pd.DataFrame({'datetime':dts})
    
    for sid in sids:
        tr[str(sid)] = 0
        
    ss = pd.DataFrame({
        'datetime x segment_id':np.concatenate([[str(x) + " x " + str(c)  
                                                for x in tr['datetime']for c in sids]]),
        'datetime':np.concatenate([[str(x) for x in tr['datetime']for c in sids]]),
        'segment_id':np.concatenate([[str(c) for x in tr['datetime']for c in sids]])
    })
    ss.head()
    
    # Add the extra features
    ss['datetime'] = pd.to_datetime(ss['datetime'])
    ss['day'] = ss['datetime'].dt.weekday_name
    ss['min'] = ss['datetime'].dt.hour*60+ss['datetime'].dt.minute
    ss = pd.merge(ss, locations, left_on='segment_id', right_on='road_segment_id', how='left')
    ss['prediction'] = 0.0
    ss.head()
    
    # Make predictions
     #model.predict_proba(test[x_cols])[:, 1]
    ss['prediction'] = model.predict_proba(ss[x_cols])[:, 1] 
    ss.head()
    
    # Changing to binary with our threshold
    # Predictions greater than the mean work pretty well
    ss['prediction'] = (ss['prediction']> ss['prediction'].mean()).astype(int)
    ss.head()
    
    
    # Save to csv and submit
    ss[['datetime x segment_id', 'prediction']].to_csv('submission.csv', index=False)
    
#make_submission()