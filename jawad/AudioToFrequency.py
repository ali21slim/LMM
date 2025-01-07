import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


audioPath=r'C:\Users\jawad\OneDrive\Desktop\E1\Research\Data 1\short derbouka examples 4-4-Audio 1.wav'
y,sr=librosa.load(audioPath,sr=None)

# This detect the onsets (when a percussion hit occurs) and convert it to time
onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

# We compute the short-time Fourier Transform and seperate the magnitude and pahse
# The phase (2D array)  determine where in each cycle the wave starts at a given time
# The magnitude (2D array) represents the amplitude of the frequency
D = librosa.stft(y) # Returns complex numbers 
magnitude, phase = librosa.magphase(D) # Rows=Frequency Bins
                                       # Columns=Time Frames

onsetFrequenciesInMidiValues = []
frequenciesFFT = librosa.fft_frequencies(sr=sr)

# We iterate over each detected onset time 
for onset in onsets:

    # convert each onset time to its corresponding frame index
    # A frame is a short segment of the audio signal that we get by slicing
    # the audio wave into small, overlapping pieces. Each slice of these is a frame.
    onsetCurrentFrame = librosa.time_to_frames(onset,sr=sr)

    # Extract the magnitude at this specific onset frame so we can get the maximum one of them
    currentOnsetMagnitude = magnitude[:,onsetCurrentFrame]

    # This returns the index of the frequency bin with the highest magnitude
    indexOfMaxMagnitude = np.argmax(currentOnsetMagnitude)

    # Based on this Bin index, we can map it to the actual frequency and transform it to MIDI unit
    frequencyAtPeak = frequenciesFFT[indexOfMaxMagnitude]
    peakFrequencyInMidi = librosa.hz_to_midi(frequencyAtPeak)

    onsetFrequenciesInMidiValues.append(peakFrequencyInMidi)
    # MIDI is a strandar protocol used in music to represent musical notes in a digital format

# Writing the results in a seperated file
lines = [f"Pulse at {onset:.2f}s: frequency = {onsetFrequenciesInMidiValues[i]:.2f} Hz\n" for i, onset in enumerate(onsets)]
with open("sample4Results.txt", 'w') as f:
    f.writelines(lines)
