# Before we begin, set the working directory because R is that lame
setwd("~/Python/GithubProjects/Zindi/Fowl Escapades/R")

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
# give this man a bells https://www.r-bloggers.com/looping-through-files/

# gets a list of all the mp3 files in the path
get_mp3_file_names = function(file_path)
{
  # only get mp3 files, don't care about the rest
  return(dir(file_path, pattern = ".mp3"))
}

train_path = "./data/Train/"
train_files.names = get_mp3_file_names(train_path)

test_path = "./data/Test/"
test_files.names = get_mp3_file_names(test_path)



# Extract something useful for our model
# If I go the spectrogram route, I should use av not tuneR
library(tuneR)
get_mfcc_from_file = function(file_path)
{
  mofo = melfcc(content, content@samp.rate, wintime=0.5)
  return(mofo)
}

for (file in test_files.names){
  str(test_path)
  str(file)
}
test_file = test_path + test_files.names[1]

# Dude uses CNN can try that
# Fit classifier to Training set



# Predict Test set results



# Test model performance



# Visualise results