# https://docs.coqui.ai/en/latest/inference.html

import torch
from TTS.api import TTS

import sys
import os
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS")
sys.path.append(project_root)

sys.path.append("/home/nim/venv/NLP-code/TTS")
sys.path.append(project_root)
from texts import *
print(sys.path)





# List available 🐸TTS models
print(TTS().list_models())


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"
# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
# wav = tts.tts(text="Hello world!", speaker_wav="/home/nim/Documents/kate_1_7.wav", language="en")

# Text to speech to a file

text = text_lost_metal


tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/kate_1_2_much_longer.wav", language="en", file_path="/home/nim/output_tress_by_much_longer_kate_TRY.wav")
# tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/michael_1_long.wav", language="en", file_path="/home/nim/output_last_metal_by_michael.wav")

tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/rebecca.wav", language="en", file_path="/home/nim/output_pumpkim_by_rebecca.wav")


tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/kate_1_2_much_longer.wav", language="en", file_path="/home/nim/output_tress_by_much_longer_kate_TRY.wav")
# tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/michael_1_long.wav", language="en", file_path="/home/nim/output_last_metal_by_michael.wav")

text = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now." Mapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'
tts.tts_to_file(text=text, speaker_wav="/home/nim/Documents/ralph.wav", language="en", file_path="/home/nim/TRY.wav")