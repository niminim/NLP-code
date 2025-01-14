import os.path

import webrtcvad
import wave



import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True).to('cuda')

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

############################


######## Detect decrease in volume

import librosa
import numpy as np
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Qt5Agg')  # or 'Qt5Agg' depending on your system

# Load the audio file
folder = '/home/nim/Lord_of_the_Necropolis_by_scott_brick_350/audio/Four'
audio_path = os.path.join(folder, "part58.wav")
audio, sr = librosa.load(audio_path, sr=None)  # sr=None retains the original sampling rate

# Calculate the RMS over short frames
frame_length = int(0.025 * sr)  # 25ms frame length
hop_length = int(0.010 * sr)  # 10ms hop size
rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]

abs_amplitude = np.abs(audio)

threshold = 0.5 * np.mean(rms)  # 50% of average RMS
low_volume_indices = np.where(rms < threshold)[0]


# Time axis for the RMS
frames = range(len(rms))
times = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)

# Plot the waveform and RMS
plt.figure(figsize=(12, 6))
plt.plot(np.linspace(0, len(audio) / sr, len(audio)), audio, alpha=0.5, label="Waveform")
plt.plot(times, rms, color="r", label="RMS (Volume)")
plt.axhline(y=threshold, color="g", linestyle="--", label="Threshold")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude / RMS")
plt.legend()
plt.title("Waveform and Volume (RMS)")
plt.show()


# Convert low-volume frame indices to time intervals
low_volume_times = librosa.frames_to_time(low_volume_indices, sr=sr, hop_length=hop_length)
print("Low-volume regions (in seconds):", low_volume_times)

intervals = librosa.effects.split(audio, top_db=20)  # Silence threshold at -20 dB
print("Speech intervals (in samples):", intervals)



