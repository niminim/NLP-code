import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')  # or 'Qt5Agg' depending on your system

audio_path = "/home/nim/output_dune_by_longer_kate.wav"  # Replace with your file path

########### 2. Objective Metrics

### Short-Time Objective Intelligibility (STOI): Evaluate the intelligibility of your TTS_code output.

# The Short-Time Objective Intelligibility (STOI) metric is widely used to evaluate the intelligibility
# of speech signals. It measures how well a degraded or synthesized signal matches the original reference speech
# in terms of intelligibility.
#Here’s how you can evaluate your TTS_code output using STOI:

from pystoi.stoi import stoi
import librosa

# Load the reference audio
ref_path = "reference_audio.wav"  # Replace with your reference file path
ref_signal, sr_ref = librosa.load(ref_path, sr=16000)  # Convert to 16 kHz if not already

# Load the TTS_code-generated audio
deg_path = "tts_audio.wav"  # Replace with your TTS_code file path
deg_signal, sr_deg = librosa.load(deg_path, sr=16000)  # Ensure the sampling rate matches

# Ensure both signals have the same duration
min_length = min(len(ref_signal), len(deg_signal))
ref_signal = ref_signal[:min_length]
deg_signal = deg_signal[:min_length]

## Compute the STOI Score
# The STOI score ranges from 0 to 1, where higher values indicate better intelligibility.

# Calculate STOI
stoi_score = stoi(ref_signal, deg_signal, sr_ref, extended=False)  # Use 'extended=True' for wider applications
print(f"STOI Score: {stoi_score:.3f}")

## Batch Processing for Multiple Files
# If you have a dataset of TTS_code audio and reference files, you can automate the STOI evaluation:

import os

# Folder paths
reference_folder = "reference_files"
tts_folder = "tts_files"

scores = []

# Process all audio pairs
for ref_file, tts_file in zip(sorted(os.listdir(reference_folder)), sorted(os.listdir(tts_folder))):
    ref_path = os.path.join(reference_folder, ref_file)
    tts_path = os.path.join(tts_folder, tts_file)

    # Load both files
    ref_signal, sr_ref = librosa.load(ref_path, sr=16000)
    tts_signal, sr_tts = librosa.load(tts_path, sr=16000)

    # Trim to the same length
    min_length = min(len(ref_signal), len(tts_signal))
    ref_signal = ref_signal[:min_length]
    tts_signal = tts_signal[:min_length]

    # Calculate STOI
    score = stoi(ref_signal, tts_signal, sr_ref, extended=False)
    scores.append((ref_file, tts_file, score))

# Display results
for ref, tts, score in scores:
    print(f"Reference: {ref}, TTS_code: {tts}, STOI Score: {score:.3f}")

## Interpret the Results:
# STOI Score ≥ 0.9: Excellent intelligibility.
# STOI Score between 0.75 and 0.9: Good intelligibility but with room for improvement.
# STOI Score < 0.75: Poor intelligibility.

## Key Considerations
# Sampling Rate: STOI assumes the signals are sampled at 16 kHz. If your audio files are at a different sampling rate, resample them using librosa.resample().
# Signal Length: Ensure both the reference and TTS_code audio files are of the same duration.
# Use Extended STOI: For more challenging scenarios (e.g., noisy environments), use extended=True.
#### End of STOI


### Mel-Cepstral Distortion (MCD): Measure the difference between your generated audio and a reference in the mel-cepstral domain.

# Mel-Cepstral Distortion (MCD) is a metric for comparing the quality of synthesized speech with a reference by calculating
# the differences in their mel-cepstral coefficients (MCCs). A lower MCD score indicates higher similarity and better quality.
# Here’s how to compute MCD step by step:

## Compute Mel-Cepstral Coefficients (MCCs)
# The MCCs are derived from the spectrum of the audio signal. We use a library like librosa to compute the spectrum and extract the coefficients.

import numpy as np
import librosa


def compute_mfcc(audio_path, sr=16000, n_mfcc=13):
    # Load audio
    y, _ = librosa.load(audio_path, sr=sr)

    # Compute MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfccs.T  # Transpose for easier frame-by-frame comparison

## Compute Mel-Cepstral Distortion (MCD)

def calculate_mcd(ref_mfcc, gen_mfcc):
    # Ensure both have the same number of frames
    min_length = min(len(ref_mfcc), len(gen_mfcc))
    ref_mfcc = ref_mfcc[:min_length]
    gen_mfcc = gen_mfcc[:min_length]

    # Calculate the squared differences
    diff = ref_mfcc - gen_mfcc
    squared_diff = np.sum(diff ** 2, axis=1)

    # MCD computation
    mcd = (10 / np.log(10)) * np.sqrt(2 * np.mean(squared_diff))
    return mcd

### Example Workflow
# Load the reference and generated audio files.
# Compute their MFCCs.
# Compute the MCD using the formula above.
# Paths to audio files
reference_audio = "reference_audio.wav"
generated_audio = "generated_audio.wav"

# Compute MFCCs
ref_mfcc = compute_mfcc(reference_audio)
gen_mfcc = compute_mfcc(generated_audio)

# Calculate MCD
mcd_score = calculate_mcd(ref_mfcc, gen_mfcc)
print(f"Mel-Cepstral Distortion (MCD): {mcd_score:.2f}")

## Batch Processing for Multiple Files
# If you have a dataset of reference and generated files, process them all:

import os

# Paths to directories
ref_dir = "reference_audio"
gen_dir = "generated_audio"

# Process all files
mcd_scores = []

for ref_file, gen_file in zip(sorted(os.listdir(ref_dir)), sorted(os.listdir(gen_dir))):
    ref_path = os.path.join(ref_dir, ref_file)
    gen_path = os.path.join(gen_dir, gen_file)

    # Compute MFCCs
    ref_mfcc = compute_mfcc(ref_path)
    gen_mfcc = compute_mfcc(gen_path)

    # Compute MCD
    mcd = calculate_mcd(ref_mfcc, gen_mfcc)
    mcd_scores.append((ref_file, gen_file, mcd))

# Display results
for ref_file, gen_file, mcd in mcd_scores:
    print(f"Reference: {ref_file}, Generated: {gen_file}, MCD: {mcd:.2f}")

## Interpret the Results
# MCD ≤ 4 dB: Very high quality; almost identical to the reference.
# MCD 4–6 dB: Good quality, acceptable for many applications.
# MCD > 6 dB: Significant differences; lower intelligibility or naturalness.

## Key Considerations
# Sampling Rate: Ensure both audio files have the same sampling rate (e.g., 16 kHz).
# MFCC Configuration: Use consistent settings for n_mfcc and other parameters.
# Signal Alignment: If the files have different durations, truncate or align them before computing MCD.
# Normalization: Preprocess the audio signals (e.g., normalization) for better comparisons.

### End of MCD
##### End of 2. Objective Metrics



############  3. Automated Tools
## Speech Analysis Libraries: Use Python libraries like librosa to analyze parameters such as pitch, energy, and duration for consistency.

# Load the audio file
audio_path = "/home/nim/output_dune_by_longer_kate.wav"  # Replace with your file path
y, sr = librosa.load(audio_path, sr=None)

print(f"Sampling Rate: {sr}, Duration: {len(y)/sr} seconds")

#### Speech Analysis
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
###  End of Speech Analysis
###### End of 3. Automated Tools



############  5. Spectrogram Analysis
# Use a spectrogram viewer to visualize your audio. Tools like matplotlib or software like Audacity allow you to see
# if there are unnatural artifacts or irregularities.

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
# TTS_code systems should produce audio with a smooth distribution of frequencies. Key points to observe:
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

# TTS_code Spectrogram
plt.subplot(2, 1, 1)
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="viridis")
plt.colorbar(format="%+2.0f dB")
plt.title("TTS_code Audio Spectrogram")

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

############  End of 5.Spectrogram Analysis


