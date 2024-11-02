from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech

import sys
import os
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS")
sys.path.append(project_root)
from texts import *


processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")

text = text_shoe_dog_mid

inputs = processor(text=text, return_tensors="pt")

from datasets import load_dataset

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

import torch

speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

spectrogram = model.generate_speech(inputs["input_ids"], speaker_embeddings)

from transformers import SpeechT5HifiGan

vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")


speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)


import soundfile as sf
filename = 'GR_book_t5'
sf.write(f"//home/nim/venv/NLP-code/TTS/{filename}.wav", speech, samplerate=22050)
print(f"Audio generated and saved as {filename}.wav'")

