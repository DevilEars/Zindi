# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:40:02 2019

@author: devilears
"""

#$$$ Hyper parameter tuning $$$
params = {'depth':[3,1,2,6,4,5,7,8,9,10],
          'iterations':[250,100,500,1000,23],
          'learning_rate':[0.03,0.001,0.01,0.1,0.2,0.3, 0.0005], 
          'l2_leaf_reg':[3,1,5,10,100],
          'border_count':[32,5,20,50,100,200],
          'ctr_border_count':[50,5,10,20,100,200],
          'thread_count':4}

# this function does 3-fold crossvalidation with catboostclassifier
from sklearn.model_selection import KFold
          
# Cross Validation Test
def crossvaltest(params,train_set,train_label,cat_dims,n_splits=3):
    kf = KFold(n_splits=n_splits,shuffle=True) 
    res = []
    for train_index, test_index in kf.split(train_set):
        train = train_set.iloc[train_index,:]
        test = train_set.iloc[test_index,:]

        labels = train_label.ix[train_index]
        test_labels = train_label.ix[test_index]

        clf = CatBoostClassifier(**params)
        clf.fit(train, np.ravel(labels), cat_features=cat_dims)

        res.append(np.mean(clf.predict(test)==np.ravel(test_labels)))
    return np.mean(res)

from paramsearch import paramsearch
from itertools import chain

# this function runs grid search on several parameters
def catboost_param_tune(params,train_set,train_label,cat_dims=None,n_splits=3):
    ps = paramsearch(params)
    # search 'border_count', 'l2_leaf_reg' etc. individually 
    #   but 'iterations','learning_rate' together
    for prms in chain(ps.grid_search(['border_count']),
                      ps.grid_search(['ctr_border_count']),
                      ps.grid_search(['l2_leaf_reg']),
                      ps.grid_search(['iterations','learning_rate']),
                      ps.grid_search(['depth'])):
        res = crossvaltest(prms,train_set,train_label,cat_dims,n_splits)
        # save the crossvalidation result so that future iterations can reuse the best parameters
        ps.register_result(res,prms)
        #print(res,prms,s'best:',ps.bestscore(),ps.bestparam())
    return ps.bestparam()


bestparams = catboost_param_tune(params,train,x_cols,cat_cols)