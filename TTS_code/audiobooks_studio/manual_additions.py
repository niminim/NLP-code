# https://docs.coqui.ai/en/latest/inference.html

import torch
from TTS.api import TTS

import os
import sys
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS_code/audiobooks_studio")
sys.path.append(project_root)
print(sys.path)


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


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




# Manual Additions
text = '\n\n\n\n\n\n\n\nPart One - The Legacy of Baron Janosk'
text = '\n\n\n\n\n\n\n\nPart Two - The Dance of Death'
text = '\n\n\n\n\n\n\n\nPart Three - The Judgment of th Fates'

text1 = '\n\n\n\n\n\n\n\nPart One - Darkon'
text2 = '\n\n\n\n\n\n\n\nPart Two - Oerth'
text3 = '\n\n\n\n\n\n\n\nPart Three - Barovia'
text4 = '\n\n\n\n\n\n\n\nPart Four - Darkon'
folder = '/home/nim/King_of_the_Dead_by_scott_brick_350'
tts.tts_to_file(text=text1, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/01_0-Part_One-Darkon.wav")
tts.tts_to_file(text=text2, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/07_0-Part_Two-Oerth.wav")
tts.tts_to_file(text=text3, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/18_0-Part_Three-Barovia.wav")
tts.tts_to_file(text=text4, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/22_0-Part_Four-Darkon.wav")
#############

import tqdm
from tools.create_models import *
from tools.clean_text import *
from tools.read_file import *
from tools.split_text import *
from tools.finalize_files import *

file_path = '/home/nim/Downloads/Lord_of_the_Necropolis.epub'
folder = '/home/nim/Lord_of_the_Necropolis_by_scott_brick_350'

tts_model = get_model(model_name ='xtts_v2')

text = read_epub(file_path)
text1 = text[-3100:-2100]
print(text1)
processed_text = process_text(text1)  # pay attention to paragraphs newlines (currently supports one and two)
chapter_chunks = efficient_split_text_to_chunks(processed_text, max_length=350)

# Generate audio and save the original text of each chunk
for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter idx {chapter_idx} - Processing chunks")):
    print(chunk)
    tts_model.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)


    # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(audio_dir, chapter_str + chapter_name + f".{audio_format}")
    concat_wavs_in_folder(chapter_audio_dir, output_file, format=audio_format)

tts_model.tts_to_file(text=processed_text, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/0-Preface.wav")
################