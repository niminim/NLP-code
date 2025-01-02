from TTS_code.api import TTS
import soundfile as sf
import numpy as np
import torch

import sys
import os
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from texts import *


# Initialize TTS_code model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"

device = "cuda" if torch.cuda.is_available() else "cpu"
# device = 'cpu'

tts = TTS(model_name).to(device)

text = text_shoe_dog


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
    audio = tts.tts(chunk)  # Generate speech for the chunk
    audio_arrays.append(audio)  # Store the audio array

# Concatenate all audio arrays into one
combined_audio = np.concatenate(audio_arrays)

# Save the combined audio to a single WAV file
output_filename = 'GR_book_concat_chunks.wav'
sf.write(f"/TTS_code/{output_filename}", combined_audio, samplerate=22050)
print(f"Audio saved as {output_filename}")


# Save the each audio array to a single WAV file
for idx, audio_arr in enumerate(audio_arrays):
    output_filename = f"output_audio_chunk_{idx + 1}.wav"
    sf.write(f"/TTS_code/{output_filename}", audio_arr, samplerate=22050)


for idx, txt in enumerate(text_chunks):
    print(f"len of chunk {idx+1}: {len(txt)}")

for idx, aud in enumerate(audio_arrays):
    print(f"len of chunk {idx + 1}: {len(aud)}")



#############
# Process each chunk with TTS_code and save to separate audio files
# for idx, chunk in enumerate(text_chunks):
#     # Generate speech audio for each chunk
#     audio = tts.tts(chunk)
#
#     # Save each chunk to a separate WAV file
#     output_filename = f"output_audio_chunk_{idx + 1}.wav"
#     sf.write(f"//home/nim/venv/NLP-code/TTS_code/{output_filename}", audio, samplerate=22050)
#     print(f"Audio generated and saved as '{output_filename}' for chunk {idx + 1}.")
#############


