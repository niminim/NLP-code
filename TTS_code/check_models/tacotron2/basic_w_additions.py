from TTS_code.api import TTS
import soundfile as sf
import numpy as np
from scipy.signal import resample
import torch

import sys
import os
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from texts import *


# Initialize TTS_code model
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name).to(device)

# The provided text
text = text_shoe_dog_short


def split_text(text, max_length=300):
    sentences = text.split('. ')
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def trim_silence(audio, threshold=1e-4):
    non_silent_indices = np.where(np.abs(audio) > threshold)[0]
    if len(non_silent_indices) == 0:
        return np.array([])  # Handle empty audio case
    return audio[non_silent_indices[0]:non_silent_indices[-1] + 1]

def generate_silence(duration, samplerate=22050):
    return np.zeros(int(duration * samplerate))

# Split text and generate audio
text_chunks = split_text(text, max_length=300)
audio_arrays = [trim_silence(tts.tts(chunk)) for chunk in text_chunks]

# Add silence between chunks to smooth transitions
silence = generate_silence(0.1)
combined_audio = np.concatenate([np.concatenate([a, silence]) for a in audio_arrays])

# Save combined audio
output_filename = 'GR_book_concat_chunks.wav'
sf.write(f"/TTS_code/{output_filename}", combined_audio, samplerate=22050)
print(f"Audio saved as {output_filename}")