"""
src.py

TODO: description of file
"""



import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt


file_path = './sample_audio/sample4.wav'
y, sr = librosa.load(file_path, sr=None)


onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

D = librosa.stft(y)

magnitude, phase = librosa.magphase(D)


onset_frequencies = []
for onset in onsets:
    onset_frame = librosa.time_to_frames(onset, sr=sr)
    
    onset_magnitude = magnitude[:, onset_frame]
    
    peak_idx = np.argmax(onset_magnitude)
    
    peak_frequency = librosa.hz_to_midi(librosa.fft_frequencies(sr=sr)[peak_idx])
    onset_frequencies.append(peak_frequency)

s=""
for i, onset in enumerate(onsets):
    s+=f"Pulse at {onset:.2f}s: frequency = {onset_frequencies[i]:.2f} Hz\n"

f=open("sample4.txt", 'w')
f.write(s)
f.close()

plt.figure(figsize=(10, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
for onset in onsets:
    plt.axvline(x=onset, color='r', linestyle='--')
plt.title('Audio Waveform with Onsets')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.show()
