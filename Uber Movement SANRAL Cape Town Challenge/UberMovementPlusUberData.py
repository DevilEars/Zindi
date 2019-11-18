# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:43:22 2019

@author: DevilEars
"""

import pandas as pd
import numpy as np

# training data and sample submission
sample_sub = pd.read_csv('data/SampleSubmission.csv')
data = pd.read_csv('data/train.csv', 
                   parse_dates = ['Occurrence Local Date Time'])

# $$$ Cleaning Training Data $$$

# These are pointless, so I'm deleting them
del data['Reporting Agency']
del data['Status']

# Remove all the longitudes named 'Closed' 
data = data[data.longitude != 'Closed']
data['road_segment_id'].unique().shape
# Change the dtype of longitudes to float
data['longitude'] = data['longitude'].apply(lambda x:float(x))


# $$$ Training and Testing Data Sets

train_data_date_to = '2018-01-01'
train_data_date_from = '2016-01-01'

train = data.loc[data['Occurrence Local Date Time'] < train_data_date_to]
train = train.loc[train['Occurrence Local Date Time'] >= train_data_date_from]

# Testing data from 2018
testing_data_date_to = '2019-01-01'
testing_data_date_from = '2018-01-01'
local_test = data.loc[data['Occurrence Local Date Time'] < testing_data_date_to]
local_test = local_test.loc[local_test['Occurrence Local Date Time'] >= testing_data_date_from]


