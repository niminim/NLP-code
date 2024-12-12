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


c0 =  'Scourge of the Wicked Kendragon\nJanet Pack\n\n\n\n\n\n\n"But I was only… aaahhhh!"\nPropelled by the shopkeeper\'s arm, the kender Mapshaker Wanderfuss became a bird, sailing through the door and thudding into the middle of Daltigoth\'s main street. Dust clouded around the kender. Indignant and coughing, he levered himself to a sitting position'
c5 = '" Mapshaker wandered into the forge area and continued his explanation. "I only tasted it. After all, one corner was hanging over the edge of the table."\n"I\'m busy. Go away," the smith said roughly, pumping the bellows until the roaring fire made conversation impossible.\nA merchant\'s messenger scurried by with a handful of accounts'
c31 = '"\nPiling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone'
c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."\n\n\n\n\n\n\n\n\n\nMapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'


c0 =  'Scourge of the Wicked Kendragon \nJanet Pack \n"But I was only… aaahhhh!" \nPropelled by the shopkeeper\'s arm, the kender Mapshaker Wanderfuss became a bird, sailing through the door and thudding into the middle of Daltigoth\'s main street. Dust clouded around the kender. Indignant and coughing, he levered himself to a sitting position'
c5 = '" Mapshaker wandered into the forge area and continued his explanation. "I only tasted it. After all, one corner was hanging over the edge of the table."  "I\'m busy. Go away," the smith said roughly, pumping the bellows until the roaring fire made conversation impossible.\nA merchant\'s messenger scurried by with a handful of accounts'
c31 = '" Piling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone'

c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."  Mapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'
c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now." New section - Mapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'
c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."  New section...Mapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'
c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."  \nNew section - Mapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'


import re
def replace_newline_after_quote(input_text):
    """
    Replaces instances of '"\n' followed by a capital letter with '" '
    and retains the capital letter.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    return re.sub(r'"\n([A-Z])', r'" \1', input_text)

input = '" Piling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone\n'

text = replace_newline_after_quote(c31)


input_text= 'Scourge of the Wicked Kendragon\nJanet Pack\n\n\n\n\n\n\n"But I was only… aaahhhh!"\nPropelled'
input_text= 'Scourge of the Wicked \nJanet Nill\n\n\n\n\n\n\n"But I was only… aaahhhh!"\nPropelled'


input_text = '”She hesitated, then said, “Very well, but'
tts.tts_to_file(text=input_text, speaker_wav="/home/nim/Documents/ralph.wav", language="en", file_path="/home/nim/TRY.wav")