from TTS.api import TTS
import soundfile as sf
import torch

import sys
import os
project_root = os.path.abspath("/TTS")
sys.path.append(project_root)
from texts import *


# 1. Initialize TTS model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"

device = "cuda" if torch.cuda.is_available() else "cpu"
# device = 'cpu'

tts = TTS(model_name).to(device)


# 2. Input text to convert to speech
# text = "Hello! This is a text-to-speech demonstration using a TTS model from Hugging Face."

text = text_shoe_dog



# 3. Generate speech audio (numpy array)
audio = tts.tts(text)

# 4. Save the generated audio to a WAV file
filename = 'GR_book'
sf.write(f"//home/nim/venv/NLP-code/TTS/{filename}.wav", audio, samplerate=22050)
print(f"Audio generated and saved as {filename}.wav'")