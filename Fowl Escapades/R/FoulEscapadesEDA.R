# This is DevilEar's first contribution to the Zindi community! 

# A blog post that accompanies this code: 

# install packages if needed
#install.packages("av")

# import libraries
library(av)

# working directory, set as needed
path <- "~/R/Zindi/Fowl Escapades"

# set working directory
setwd(path) 



# $$$$$$ Load datasets $$$$$$

# this dataset just contains a handful of samples
# I have placed the samples in their own zip file
# you need to download that file and extract it for any
# of this to work
file_name <- "EDASamples.csv"
eda_samples <- read.csv(file_name, header = FALSE)
  


# $$$$$$ Basic EDA $$$$$$

# I made the EDA Samples file myself, so it's very ideal.
# These are added in case you want to explore the competition data

# peek inside
dim(eda_samples)

# check the variables and their types
str(eda_samples)

# check for null values
table(is.na(eda_samples))

summary(eda_samples)



# $$$$$$ Audio Signals EDA $$$$$$

# EDA in time domain
# TODO fix file path once I have samples 
audio_file <- "~/R/Zindi/Fowl Escapades/EDASamples/ds5B591U.mp3"


# show some audio information with the av package
av_media_info(audio_file)

# read 3 sec of data and plot the waveform
pcm_data <- read_audio_bin(audio_file, channels = 1, end_time = 3.0)
plot(pcm_data, type = 'l')

# look at some metrics, some EDA yay!
dim(pcm_data)
str(pcm_data)
summary(pcm_data)

# read 3 sec of data and directly transform to frequency
# plot the spectrogram
fft_data <- read_audio_fft(audio_file, end_time = 3.0)
plot(fft_data)

# look at some metrics
dim(fft_data)
str(fft_data)


# EDA in frequency domain
# from:  https://www.cs.tut.fi/sgn/arg/intro/basics.html
#u = s(0.2 * fs:0.2 * fs + 511) .* hanning(512);
#U = fft(u);
#f = (0:256) / 256 * fs / 2;
#plot(f, 20 * log10(abs(U(1:257))))

# FFT on bird call

# plot the transformed data

# look at some metrics



# $$$$$$ Windows and filters $$$$$$
# There are many more avaiable windows and filters in the signals package


