# Uber Movement SANRAL Cape Town Challenge
Note that I have skipped all the [data files](https://zindi.africa/competitions/uber-movement-sanral-cape-town-challenge/data), since I do not wish to clog my git repo with all kinds of data files.

## Starter code
This code is initially based on the [starter notebook](https://colab.research.google.com/drive/1HjJhghj2b5JJnOFNTcojLfAicDf5QWWK#scrollTo=F7CulRNdygp_&forceEdit=true&sandboxMode=true) from the Zindi forums.

## My approach
1. Remember to train on the entire data set and not just on the segments in the sample notebook.
1. [Data cleaning](https://towardsdatascience.com/data-cleaning-101-948d22a92e4), the bane of my existence. The training data features a few dodgy entries already. I would need a few methods to ensure that my model is robust enough to deal with dodgy entries. For starters, I just removed the dodgy entries from the training set since they were only a handful, but I will not be able to rely on my own fair hands in all case.
1. [Hyper parameter tuning](https://effectiveml.com/using-grid-search-to-optimise-catboost-parameters.html) is a trusty rusty ally. I inserted this as soon as I had a working build that delivers commits. This is because I want this to be part of my model already, before I start throwing more features at it and before I start exploring different datasets. Of course this means more variables to take into account, so when it comes to comparing different models, it is more wise to test them with the same parameters. For this reason, I added the hyper parameter tuning in such a way that it can easily be removed. CatBoost is pretty good, though.
1. [Exploratory data analysis](https://github.com/thusodangersimon/sanral_hack/blob/master/notebooks/EDA.ipynb) has been kindly done by another contestant. There may be more insights to be gained by doing further plotting, so this is something to consider later on.	
