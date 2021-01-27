import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks

chunk = 1024  
sample_format = pyaudio.paInt16  
channels = 2
fs = 44100  
seconds = 2
filename = "output.wav"


while True:
    p = pyaudio.PyAudio()
    print("Press enter button to start recording...")
    s = input()
    print('Recording')

    stream = p.open(
        format = sample_format,
        channels = channels,
        rate = fs,
        frames_per_buffer = chunk,
        input = True
    )

    frames = []

    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    import librosa
    import matplotlib.pyplot as plt
    import librosa.display
    from matplotlib.pyplot import specgram

    x, sr = librosa.load('output.wav')

    plt.figure(figsize=(2.24, 2.24), dpi = 100)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0, 0) 

    spectrogram = librosa.feature.melspectrogram(y = x, sr = sr, n_mels = 128, fmax =8000) 
    spectrogram = librosa.power_to_db(spectrogram)

    librosa.display.specshow(spectrogram, y_axis = None, fmax = None, x_axis = None)
    plt.title(None)

    import random

    def rand(length = 40):
        s = list("abcdefghiklmnopqrstuvwxyz1234567890")
        p = ""
        for i in range(length):
            p += random.choice(s)
        return p

    folder = "Left"
    plt.savefig(f'{folder}/{rand()}.png')

    import os
    os.remove('output.wav')
