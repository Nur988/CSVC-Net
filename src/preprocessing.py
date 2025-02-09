import os
import librosa
from tqdm import tqdm
import pandas as pd
import numpy as np
from scipy.io import wavfile
import random


def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window = int(rate/10), min_periods = 1, center = True).mean()
    
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask        

# Preparing Training Data
audio_dir = "/content/drive/MyDrive/PR/allrecordings/"
file_names = [f for f in os.listdir(audio_dir) if '.wav' in f]
random.shuffle(file_names)
train_file_names=file_names[1:1800]

# Preparing clean training set
for f in tqdm(train_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    mask = envelope(signal, rate, 0.0005)
    wavfile.write(filename = "/content/drive/MyDrive/PR/cleantrain/" + f, rate = rate, data = signal[mask])
    # wavfile.write(filename = "/content/drive/MyDrive/PR/cleantrain/" + f, rate = rate, data = signal[mask])

audio_dir = "/content/drive/MyDrive/PR/cleantrain/"
clean_file_names = [f for f in os.listdir(audio_dir) if '.wav' in f]


# pitch_shift_low
for f in tqdm(clean_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_pitch_sf = librosa.effects.pitch_shift(signal,rate,n_steps=-5)
    wavfile.write(filename = "/content/drive/MyDrive/PR/train/" + f + '_pitch_shift', rate = rate, data = wav_pitch_sf)

# pitch_shift_high
for f in tqdm(clean_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_pitch_sf = librosa.effects.pitch_shift(signal,rate,n_steps=5)
    wavfile.write(filename = "/content/drive/MyDrive/PR/train/" + f + '_pitch_shift_pos', rate = rate, data = wav_pitch_sf)
    
#time_strech_fast
for f in tqdm(clean_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_time_stch = librosa.effects.time_stretch(signal,1.2)
    wavfile.write(filename = "/content/drive/MyDrive/PR/train/" + f + '_time_stretch_fast', rate = rate, data = wav_time_stch )

#time_strech_slow
for f in tqdm(clean_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_time_stch = librosa.effects.time_stretch(signal,0.6)
    wavfile.write(filename = "/content/drive/MyDrive/PR/train/" + f + '_time_stretch_slow' + f, rate = rate, data = wav_time_stch )

#add noise
for f in tqdm(clean_file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_n = signal + 0.001*np.random.normal(0,1,len(signal))
    wav_n = wav_n.astype(type(signal[0]))
    wavfile.write(filename = "/content/drive/MyDrive/PR/train/" + f + '_noisy', rate = rate, data = wav_n )


#Preparing Test Data
# audio_dir = "./testset/"
# file_names = [f for f in os.listdir(audio_dir) if '.wav' in f]
test_file_names=file_names[1800:]
# Preparing clean test set
for f in tqdm(test_file_names):
    print(f)
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    mask = envelope(signal, rate, 0.0005)
    wavfile.write(filename = "/content/drive/MyDrive/PR/cleantest/" + f, rate = rate, data = signal[mask])

# Preparing noisy test set
audio_dir = "/content/drive/MyDrive/PR/cleantest/"
file_names = [f for f in os.listdir(audio_dir) if '.wav' in f]
for f in tqdm(file_names):
    signal, rate = librosa.load(audio_dir + f, sr = 16000)
    wav_n = signal + 0.001*np.random.normal(0,1,len(signal))
    wav_n = wav_n.astype(type(signal[0]))
    wavfile.write(filename = "/content/drive/MyDrive/PR/test/" + f + '_noisy', rate = rate, data = wav_n )
