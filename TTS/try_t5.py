from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")

text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan. Selling the shoes from the trunk of his lime green Plymouth Valiant,
Knight grossed $8,000 his first year. Today, Nike’s annual sales top $30 billion. In an age of startups, Nike is the ne plus ultra
of all startups, and the swoosh has become a revolutionary, globe-spanning icon, one of the most ubiquitous and recognizable
symbols in the world today."""

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

