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



input = '" Piling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone\n'



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

text11 = '\n\n\n\n\n\n\n\nPart One - Into The Past'
text22 = '\n\n\n\n\n\n\n\nPart Two - The Final Search'
text33 = '\n\n\n\n\n\n\n\nPart Three - The Coming of Necropolis'
text_name = 'You are listening to Lord of the Necropolis. A Ravenloft novel, Written by Gene DeWees. Narrated by AI voice-cloning of Scott Brick'

folder = '/home/nim/To_Sleep_With_Evil'
tts.tts_to_file(text=text11, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/01_0-Part_One-Into_The_Past.wav")
tts.tts_to_file(text=text22, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/12_0-Part_Two-The_Final_Search.wav")
tts.tts_to_file(text=text33, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/21_0-Part_Three-The_Coming_of_Necropolis.wav")
# tts.tts_to_file(text=text4, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/22_0-Part_Four-Darkon.wav")
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-book.wav")


folder = '/home/nim/To_Sleep_With_Evil'
text_name = 'You are listening to the book To Sleep With Evil. A Ravenloft novel, Written by Andrial Cardarelle. Narrated by AI voice-cloning of Scott Brick'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-book.wav")


folder = '/home/nim/Shadowborn'
text_name = 'You are listening to the book - Shadowborn. A Ravenloft novel, Written by William W. Connors and Carrie A. Bebris. Narrated by AI voice-cloning of Scott Brick'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-book.wav")


folder = '/home/nim/Black_Crusade_by_scott_brick_250'
text_name = 'You are listening to - Dominion - Black Crusade. A Ravenloft novel written by Ari Marmell. Narrated by AI voice-cloning of Scott Brick'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-book.wav")

folder = '/home/nim/Mithras_Court_by_scott_brick_250'
text_name = 'You are listening to - Dominion - Mithras Court. A Ravenloft novel written by David A. Page. Narrated by AI voice-cloning of Scott Brick'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-book.wav")


folder = '/home/nim/Mithras_Court_by_scott_brick_250'
text_name = 'December, 1892 London\n\n'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/00-December_london.wav")


folder = '/home/nim/Mithras_Court_by_scott_brick_250'
text_name = '\n\n\nMithras Court\n\n\n'
tts.tts_to_file(text=text_name, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/02_0-Mithras_Court.wav")
#############

