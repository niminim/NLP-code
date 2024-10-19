# https://github.com/idiap/coqui-ai-TTS

import torch
from TTS.api import TTS
import soundfile as sf

# Initialize the XTTS-v2 model
device = "cuda" if torch.cuda.is_available() else "cpu"
device = 'cpu'
tts = TTS(model_name="tts_models/en/xtts_v2", progress_bar=False).to(device)


# 2. Input text to convert to speech
# text = "Hello! This is a text-to-speech demonstration using a TTS model from Hugging Face."

text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan.
"""

# 3. Generate speech audio (numpy array)
filename = 'GR_book_xtts_v2_short'
tts.tts_to_file(text=text, speaker_wav="my/cloning/audio.wav", language="en", file_path=f"//home/nim/venv/NLP-code/TTS/{filename}.wav")


# 4. Save the generated audio to a WAV file
sf.write(f"//home/nim/venv/NLP-code/TTS/{filename}.wav", audio, samplerate=22050)
print(f"Audio generated and saved as {filename}.wav'")