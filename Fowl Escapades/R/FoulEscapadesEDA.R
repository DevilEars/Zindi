# This is DevilEar's first contribution to the Zindi community! 

# A blog post that accompanies this code: 
# https://dev.to/devilears/zindi-fowl-escapades-challenge-eda-of-audio-data-in-r-ejj

# install if needed
#install.packages("av")
# import regardless
library(av)



# $$$$$$ Load datasets $$$$$$

# This dataset is contrived, it doesn't do anything
file_name <- "./csv/EDASamples.csv"
eda_samples <- read.csv(file_name)
  


# $$$$$$ Basic EDA $$$$$$

# I made the EDA Samples file myself, so it's very ideal.
# These are added in case you want to explore the competition data

# peek inside
dim(eda_samples)

# check for null values. decide what to do with them at this point
table(is.na(eda_samples))



# $$$$$$ Audio Signals EDA $$$$$$

# EDA in time domain
# I just used a single file for clarity and for saving space
audio_file <- "./data/EDASamples/ds5B591U.mp3"


# show some audio information with the av package
av_media_info(audio_file)

# read 3 seconds of data and plot the waveform with lines instead of dots
pcm_data <- read_audio_bin(audio_file, channels = 1, end_time = 3.0)
plot(pcm_data, type = 'l')

# look at some metrics, some EDA yay!
dim(pcm_data)
# minimum, .., Median, Mean, .. max. that sort of thing
# this is all on amplitude samples of raw audio
summary(pcm_data)

# read 3 seconds of data and directly transform to time-frequency domain
# get the spectrogram
fft_data <- read_audio_fft(audio_file, end_time = 3.0)
# look at some metrics
dim(fft_data)
str(fft_data)
# plot
plot(fft_data)



# $$$$$$ Windows and filters $$$$$$
# I used a tukey window. You can play around with
# the values, with 256 being a minimum window size
tukey_filter_data <- read_audio_fft(audio_file, end_time = 3.0, tukey(512))
# look at some metrics
dim(tukey_filter_data)
str(tukey_filter_data)
#plot
plot(tukey_filter_data)



