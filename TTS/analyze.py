import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')  # or 'Qt5Agg' depending on your system

# Load the audio file
audio_path = "/home/nim/output_dune_by_longer_kate.wav"  # Replace with your file path
y, sr = librosa.load(audio_path, sr=None)

print(f"Sampling Rate: {sr}, Duration: {len(y)/sr} seconds")

### 3. Analyze Parameters
## (a) Pitch
# You can extract the fundamental frequency (pitch) using librosa.pyin:

f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=300, sr=sr)
plt.plot(f0, label="Pitch (Hz)")
plt.xlabel("Frames")
plt.ylabel("Frequency (Hz)")
plt.title("Pitch Contour")
plt.legend()
plt.show()

# fmin and fmax set the range for pitch detection. Adjust these based on the speaker or tone.

## (b) Energy
# Energy can be computed as the squared sum of the signal over short frames:
frame_length = 2048
hop_length = 512

# Calculate energy
energy = np.array([
    sum(abs(y[i:i + frame_length] ** 2))
    for i in range(0, len(y), hop_length)
])

plt.plot(energy, label="Energy")
plt.xlabel("Frames")
plt.ylabel("Energy")
plt.title("Energy Contour")
plt.legend()
plt.show()

## (c) Duration
# Calculate the total duration of the audio:
duration = librosa.get_duration(y=y, sr=sr)
print(f"Audio Duration: {duration:.2f} seconds")

#### 4. Visualize the Audio
# A spectrogram can help identify issues in your audio signal:

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log")
plt.colorbar(format="%+2.0f dB")
plt.title("Log-Scale Spectrogram")
plt.show()

### 5. Combine with Statistical Analysis
# For consistency, compute metrics like:
# Mean and variance of pitch: Check if there's too much or too little variation.
# Standard deviation of energy: Analyze fluctuations in loudness.

mean_pitch = np.nanmean(f0)
std_pitch = np.nanstd(f0)
mean_energy = np.mean(energy)
std_energy = np.std(energy)

print(f"Mean Pitch: {mean_pitch:.2f} Hz, Std Pitch: {std_pitch:.2f} Hz")
print(f"Mean Energy: {mean_energy:.2f}, Std Energy: {std_energy:.2f}")