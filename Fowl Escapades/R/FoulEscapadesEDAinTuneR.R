# This is DevilEar's R starter code contribution to the Zindi community
# Maybe. I mean I want to 

# A blog post to accompany this code:

install.packages("tuneR")
library(tuneR)
#library(signal)

#~\Documents\Python\GithubProjects\Zindi\Fowl Escapades\R


# $$$$$$ Get the Data $$$$$$
# the pdf manual for tuneR is very good
# but this is even more hande https://hansenjohnson.org/post/spectrograms-in-r/

# mark this as the day on which I learnt that you can use = as the assignment operator in R 
# instead of -> these annoying arrows all the time

audio_file = "./data/EDASamples/0IC96G.mp3"

# this converts it to wav because MP3 is shyte
content = readMP3(audio_file)

# see if this yielded anything
summary(content)

# $$$$$$ Extract features from the Data $$$$$$

# first, let's redo my EDA because tuneR is more powerful
# and it also uses signal, so that's 2 birds and 1 stone and 2 girls and 1 cup

# the Wave object is in stereo
# we probably only need one channel for our models
snd = content@right

# plot the waveform. so sexy
plot(snd, type='l', xlab='Samples', ylab='Amplitude')



# plot the spectrogram. much better than the av package way!
# may need to wrangle the samples a bit as this is huge
#spec = specgram(content@right, content@samp.rate, window = hanning(512))
#spec = specgram(content@right, n=512, Fs=content@samp.rate, window = hanning(512))

step = trunc(5*content@samp.rate/1000)             # one spectral slice every 5 ms
window = trunc(40*content@samp.rate/1000)          # 50 ms data window
fftn = 2^ceiling(log2(abs(window))) # next highest power of 2
spg = specgram(content@right, fftn, content@samp.rate, window, (window-step))
plot(spg)

# extract the MFCC malfeasance
# someone made this uber sexy since it already extracts only 1 channel - cha!
# see https://cran.r-project.org/web/packages/tuneR/tuneR.pdf
# Usage:
#melfcc(samples, sr = samples@samp.rate, wintime = 0.025,
#       hoptime = 0.01, numcep = 12, lifterexp = 0.6, htklifter = FALSE,
#       sumpower = TRUE, preemph = 0.97, dither = FALSE,
#       minfreq = 0, maxfreq = sr/2, nbands = 40, bwidth = 1,
#       dcttype = c("t2", "t1", "t3", "t4"),
#       fbtype = c("mel", "htkmel", "fcmel", "bark"), usecmp = FALSE,
#       modelorder = NULL, spec_out = FALSE, frames_in_rows = TRUE)

# don't do this. it needs 12 Gb. Ewps
# mofo = melfcc(content, content@samp.rate, wintime=3.00)

mofo = melfcc(content, content@samp.rate, wintime=0.5)
#summary(mofo)

plot(mofo, type ='l')

# store the extracted features so I can just load this in future


# $$$$$$ Convert features for model $$$$$$



# $$$$$$ The Model, thank you Kraftwerk $$$$$$