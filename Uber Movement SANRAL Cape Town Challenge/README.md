# Uber Movement SANRAL Cape Town Challenge
Note that I have skipped all the [data files](https://zindi.africa/competitions/uber-movement-sanral-cape-town-challenge/data), since I do not wish to clog my git repo with all kinds of data files.

## Starter code
This code is initially based on the [starter notebook](https://colab.research.google.com/drive/1HjJhghj2b5JJnOFNTcojLfAicDf5QWWK#scrollTo=F7CulRNdygp_&forceEdit=true&sandboxMode=true) from the Zindi forums.

## My approach
1. Train on the entire test data set.
1. [Data cleaning](https://towardsdatascience.com/data-cleaning-101-948d22a92e4), the bane of my existence. The training data features a few dodgy entries already. I would need a few methods to ensure that my model is robust enough to deal with dodgy entries. I do remove the dodgy entries in code,
but this is not necessarily robust enough for unknown unknowns.
1. [Exploratory data analysis](https://github.com/thusodangersimon/sanral_hack/blob/master/notebooks/EDA.ipynb) has been kindly done by another contestant. There may be more insights to be gained by doing further plotting, so this is something to consider.
1. Implement the different data sets.	
1. [Hyper parameter tuning](https://effectiveml.com/using-grid-search-to-optimise-catboost-parameters.html) is a trusty rusty ally. CatBoost is pretty good, though. I will consider this at a later stage, once I have incorporated all the data sets.

## Some thoughts and prayers
1. The Sanral data appears virtually useless. It does give one an impression of incidents, but the dates follow no discernible pattern. Is it worthwhile to even look at it, instead of say more feature engineering? I think not.
1. The Uber data does not record incidents, but it does give one an idea of when congestion occurs. Reasonably, more congestion means more chance of an incident. By the same token, more congestion follows an incident. Could be useful, but cumbersome to download the data.
1. It might be worthwhile to have another look at the sample submission to see what kind of data they are looking for. A hunch is that all the incidents recorded would be an incident that they want, so a cheap and sneaky way to boost performance scores is just to say hey, there is an incident here so let's register that as a prediction. This will probably not work on the full test data set, though.
1. It's well and good to start off with starter code, but maybe going through the motions of a [data science primer](https://elitedatascience.com/primer) would yield better results or more original insights.
