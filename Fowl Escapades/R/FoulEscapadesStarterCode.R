# Before we begin, set the working directory because R is that lame
#setwd("~/Python/GithubProjects/Zindi/Fowl Escapades/R")

# Import datasets

# Submission has a matrix of all the possible matches
# You need to provide a probability between 0 and 1 for
# the likelihood of a match

# Eg a sample of an Afrian Rock Pipit should have 1 in that column 
# and 0 in all the other columns
submission = read.csv("./csv/SampleSubmission.csv")
#str(submission)

# This contains samples of each bird call
train = read.csv("./csv/Train.csv")
#str(train)



# Prepare the files
# get the column names from the submission to name my birds
birds = colnames(submission)
# Remove the 1st item which is 'ID' and I know that already
birds = birds[-1]
#str(birds)

# Add file names to the dataframes
# see how easy this is in python?
# train['file_name'] = './data/Train/' + train['ID'] + '.mp3'
# submission['file_name'] = './data/Test/' + submission['ID'] + 'mp3'

# Although this is not strictly necessary, I just need to
#process each file in those directories. Might as well do that in a loop



# Extract something useful for our model



# Fit classifier to Training set



# Predict Test set results



# Test model performance



# Visualise results