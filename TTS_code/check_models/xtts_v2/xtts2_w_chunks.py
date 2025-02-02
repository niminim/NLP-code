# https://docs.coqui.ai/en/latest/inference.html

import torch
from TTS.api import TTS
import soundfile as sf
import numpy as np

import sys
import os
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from texts import *


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"

# Init TTS_code
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


text = text_lost_metal

# Function to split text into manageable chunks if necessary
def split_text(text, max_length=300):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# Split text if it's too long for one go
text_chunks = split_text(text, max_length=300)

# List to store audio arrays
audio_arrays = []

# Process each chunk and generate audio
for idx, chunk in enumerate(text_chunks):
    wav = tts.tts(text=chunk, speaker_wav="/home/nim/Documents/kate_1_2_much_longer.wav", language="en")
    audio_arrays.append(wav)  # Store the audio array

# Concatenate all audio arrays into one
combined_audio = np.concatenate(audio_arrays)

# Save the combined audio to a single WAV file
output_filename = 'concat_last_metal_ref_kate_1_2_much_longer.wav'
sf.write(f"//home/nim/{output_filename}", combined_audio, samplerate=22050)
print(f"Audio saved as {output_filename}")

