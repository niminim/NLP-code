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
        model = TTS(model_name)
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




####################################
from TTS.api import TTS
from transformers import BarkModel, BarkProcessor

import soundfile as sf
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(TTS().list_models())

text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan.
"""


tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)
wav = tts_model.tts(text=text)
# tts_model = TTS( "tts_models/en/ljspeech/vits").to(device)
tts_model = TTS( "tts_models/en/ljspeech/glow-tts").to(device)
wav = tts_model.tts(text=text)
tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
wav = tts_model.tts(text=text, speaker_wav="/home/nim/Documents/amanda.wav", language="en")


# 4. Save the generated audio to a WAV file
filename = 'TRY_models'
sf.write(f"//home/nim/{filename}.wav", wav, samplerate=22050)
print(f"Audio generated and saved as {filename}.wav'")


# Bark is not that good in 0.25.1, also switches male and female
# # Load the model to GPU
# # Bark is really slow on CPU, so we recommend using GPU.
# tts = TTS("tts_models/multilingual/multi-dataset/bark").to("cuda")
# # random speaker
# tts.tts_to_file(text, file_path="/home/nim/try_bark.wav")



from huggingface_hub import HfApi

# Initialize the API
api = HfApi()

# Search for models related to TTS
models = api.list_models(filter="text-to-speech")
for model in models:
    print(model.modelId)

