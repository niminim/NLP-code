import torch
from TTS.api import TTS

def get_model(model_name ='xtts_v2'):

    if model_name == 'xtts_v2':
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return model

