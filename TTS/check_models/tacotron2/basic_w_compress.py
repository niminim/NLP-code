from TTS.api import TTS
import soundfile as sf
import subprocess

import sys
import os
project_root = os.path.abspath("/TTS")
sys.path.append(project_root)
from texts import *


# Initialize TTS model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"

tts = TTS(model_name)

# The provided text (shortened for demonstration)
text = text_shoe_dog

# Generate the audio as a numpy array
audio = tts.tts(text)

# Save the audio as a WAV file (temporary)
temp_wav_file = "temp_GR_book_long.wav"
sf.write(f"//home/nim/venv/NLP-code/TTS/{temp_wav_file}", audio, samplerate=22050)  # Use 16kHz for smaller size

# Compress the WAV to MP3 using FFmpeg
output_mp3_file = "GR_book_long_mp3.mp3"
bitrate = "64k"  # Adjust bitrate for desired quality and size
subprocess.run([
    "ffmpeg", "-y", "-i", temp_wav_file,  # Input temporary WAV file
    "-ac", "1",                           # Convert to mono
    "-b:a", bitrate,                      # Set bitrate
    f"//home/nim/venv/NLP-code/TTS/{output_mp3_file}"                       # Output MP3 file
])

print(f"Compressed audio saved as '{output_mp3_file}'")