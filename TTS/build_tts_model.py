from TTS.api import TTS
from transformers import BarkModel, BarkProcessor

import soundfile as sf
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = 'xtts_v2'

# List available 🐸TTS models

def build_model(model_name, device):
    print(TTS().list_models())
    if model_name == 'tacotron2':
        model_name = "tts_models/en/ljspeech/tacotron2-DDC"
        model = TTS(model_name).to(device)
    elif model_name == 'xtts_v2':
        model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    elif model_name == 'bark_small':
        # https://huggingface.co/suno/bark#example
        bark_model = BarkModel.from_pretrained("suno/bark-small")
        bark_processor = BarkProcessor.from_pretrained("suno/bark-small")

    tts_model = model.to(device)
    return tts_model




# add a speaker embedding
inputs = processor("This is a test!", voice_preset="v2/en_speaker_3")

wav = tts.tts(text=chunk, speaker_wav="/home/nim/Documents/kate_1_2_much_longer.wav", language="en")

