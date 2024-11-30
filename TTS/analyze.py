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

############  Speech Analysis
### Analyze Parameters
## Pitch
# You can extract the fundamental frequency (pitch) using librosa.pyin:

f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=50, fmax=300, sr=sr)
plt.plot(f0, label="Pitch (Hz)")
plt.xlabel("Frames")
plt.ylabel("Frequency (Hz)")
plt.title("Pitch Contour")
plt.legend()
plt.show()

# fmin and fmax set the range for pitch detection. Adjust these based on the speaker or tone.

## Energy
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

## Duration
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

### Combine with Statistical Analysis
# For consistency, compute metrics like:
# Mean and variance of pitch: Check if there's too much or too little variation.
# Standard deviation of energy: Analyze fluctuations in loudness.

mean_pitch = np.nanmean(f0)
std_pitch = np.nanstd(f0)
mean_energy = np.mean(energy)
std_energy = np.std(energy)

print(f"Mean Pitch: {mean_pitch:.2f} Hz, Std Pitch: {std_pitch:.2f} Hz")
print(f"Mean Energy: {mean_energy:.2f}, Std Energy: {std_energy:.2f}")
############  End of Speech Analysis

############  Spectrogram Analysis

## Generate a Basic Spectrogram
# Compute the Short-Time Fourier Transform (STFT)
stft = librosa.stft(y)

# Convert amplitude to decibels (dB) for better visualization
D = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

# Display the spectrogram
plt.figure(figsize=(12, 6))
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="viridis")
plt.colorbar(format="%+2.0f dB")
plt.title("Log-Scale Spectrogram")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()

## Inspect Frequency Range
# TTS systems should produce audio with a smooth distribution of frequencies. Key points to observe:
#
# Low Frequencies (50-300 Hz): These correspond to the fundamental frequencies (pitch).
# Mid Frequencies (300-3000 Hz): Critical for speech intelligibility.
# High Frequencies (3000+ Hz): Contribute to the naturalness and richness of sound.
# Check if:
#
# Frequencies are evenly distributed or have unnatural gaps.
# There's excessive energy in high or low frequencies, which might indicate artifacts.

## Analyze Harmonics and Noise
# Harmonics appear as evenly spaced horizontal lines in the spectrogram:
#
# Smooth, clear harmonics suggest natural and high-quality speech.
# Jagged or irregular harmonics indicate distortions.
# Random, spread-out noise may suggest encoding issues or artifacts.


## Focus on Transients and Pauses
# Transients: Sudden changes in the spectrogram (e.g., consonants) should be sharp and distinct.

# Pauses and Silences: Inspect the spectrogram for regions with no energy (black areas).
# Ensure these correspond to expected silences in the speech.

## Zoom In on Specific Time Intervals
# Zooming in on specific sections of the spectrogram can help analyze phoneme-level quality.
# Focus on a specific time range
start_time = 1.0  # in seconds
end_time = 2.0    # in seconds

start_sample = int(start_time * sr)
end_sample = int(end_time * sr)

D_zoom = librosa.amplitude_to_db(np.abs(librosa.stft(y[start_sample:end_sample])), ref=np.max)

plt.figure(figsize=(12, 6))
librosa.display.specshow(D_zoom, sr=sr, x_axis="time", y_axis="log", cmap="plasma")
plt.colorbar(format="%+2.0f dB")
plt.title(f"Zoomed Spectrogram from {start_time}s to {end_time}s")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()

## Compare Against Ground Truth or Baseline
# If you have a reference audio file, compare their spectrograms:
#
# Load both audio files and generate their spectrograms.
# Look for differences in frequency coverage, intensity, or artifacts.
# Load reference file
y_ref, sr_ref = librosa.load("reference_audio.wav", sr=None)

# Generate spectrogram for reference
D_ref = librosa.amplitude_to_db(np.abs(librosa.stft(y_ref)), ref=np.max)

# Plot the comparison
plt.figure(figsize=(12, 6))

# TTS Spectrogram
plt.subplot(2, 1, 1)
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="viridis")
plt.colorbar(format="%+2.0f dB")
plt.title("TTS Audio Spectrogram")

# Reference Spectrogram
plt.subplot(2, 1, 2)
librosa.display.specshow(D_ref, sr=sr_ref, x_axis="time", y_axis="log", cmap="magma")
plt.colorbar(format="%+2.0f dB")
plt.title("Reference Audio Spectrogram")

plt.tight_layout()
plt.show()


## Use Mel-Spectrograms for Speech
# Mel-spectrograms focus on perceptual frequency scales, ideal for speech analysis:
# Compute Mel-spectrogram
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
mel_spec_db = librosa.amplitude_to_db(mel_spec, ref=np.max)

# Plot Mel-spectrogram
plt.figure(figsize=(12, 6))
librosa.display.specshow(mel_spec_db, sr=sr, x_axis="time", y_axis="mel", cmap="coolwarm")
plt.colorbar(format="%+2.0f dB")
plt.title("Mel-Spectrogram")
plt.xlabel("Time (s)")
plt.ylabel("Mel Frequency")
plt.show()

## What to Look For in the Spectrogram?
# Artifacts: Sudden spikes or irregular bands.
# Smoothness: Even energy transitions over time.
# Frequency Coverage: Ensure the audio covers expected ranges without gaps.
# Temporal Consistency: Ensure no unexpected jumps or dips in intensity.
# Would you like a complete script to process multiple audio files or analyze specific patterns?

############  End of Spectrogram Analysis
