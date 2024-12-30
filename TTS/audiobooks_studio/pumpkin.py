import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from pydub import AudioSegment
import os
import time

from tqdm import tqdm

import torch
from TTS.api import TTS



def efficient_split_text_to_chunks(text, max_length): # this was used and worked
    """
    Splits the text into the largest possible chunks based on the assigned maximum length,
    ensuring each chunk ends at a sentence boundary ('.') when possible.
    If no '.' is found, splits at the nearest whitespace to avoid breaking words.

    Args:
        text (str): The input text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        # Determine the furthest point for the current chunk
        end = min(start + max_length, len(text))

        # Look for the last '.' within the allowable range
        last_dot_index = text.rfind(".", start, end)

        if last_dot_index == -1:  # If no '.' is found in the range
            # Look for the last whitespace within the range
            last_space_index = text.rfind(" ", start, end)
            if last_space_index != -1:  # If a space is found, split at the space
                last_dot_index = last_space_index
            else:  # If no space is found, split at the max length
                last_dot_index = end

        # Add the chunk
        chunks.append(text[start:last_dot_index].strip())
        # Update the start to the new position
        start = last_dot_index + 1

    return [chunk for chunk in chunks if chunk]  # Remove any empty chunks


######## Clean text
def replace_newline_sequences(input_text):
    # Replace 3 or more newline characters with "  An ornamental break  ."
    return re.sub(r'\n{3,}', '  ', input_text)


def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    - Example: Replace sequences of 5+ newlines with 'New section - '.
    """
    return re.sub(r'\n{4,}', ' New section - ', chunk)


def process_chunk_replace_quotes_newline(input_text):
    """
    Replaces instances of '"' followed by '\n' followed by '"' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    return re.sub(r'"\n"', '" "', input_text)

def replace_right_quote_newline(input_text):
    """
    Replaces instances of '”\n' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    return re.sub(r'”\n', ' ', input_text)


def process_chunk_replace_quotes_newlines(input_text):
    """
    Replaces instances of '"' followed by one or more '\n' characters followed by '"' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    return re.sub(r'"\n{1,}"', '" "', input_text)


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

def fix_punctuation_spacing(text):
    """
    Replaces all occurrences of '."' with '".' in the input text.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with corrected punctuation.
    """
    return text.replace('."', '".')


######## End of Clean text


def concat_wavs_in_folder(folder_path, output_file, format='wav'):
    """
    Concatenates all WAV files in a folder in numerical order based on the part number
    in their filenames and saves them into a single WAV file.

    Args:
        folder_path (str): Path to the folder containing WAV files.
        output_file (str): Path to save the combined WAV file.

    Returns:
        None
    """
    # Function to extract the numeric part from the filename
    def extract_number(file_name):
        match = re.search(r'part(\d+)', file_name, re.IGNORECASE)
        return int(match.group(1)) if match else float('inf')  # Place non-matching files at the end

    # List all WAV files in the folder
    wav_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]

    # Sort files numerically based on the extracted number
    sorted_files = sorted(wav_files, key=extract_number)

    # Initialize an empty AudioSegment for concatenation
    combined = AudioSegment.empty()

    # Concatenate the sorted audio files
    for file_name in sorted_files:
        file_path = os.path.join(folder_path, file_name)
        print(f"Adding {file_name} to the combined audio.")
        audio = AudioSegment.from_wav(file_path)
        combined += audio

    # Export the combined audio to the specified output file
    if format.lower() == 'wav':
        combined.export(output_file, format="wav")
    elif format.lower() == 'mp3':
        combined.export(output_file, format="mp3", bitrate="320")
    print(f"All WAV files concatenated and saved as '{output_file}'.")
######## End of Finalize files


#############################################################################

text = """
"And that's where we're supposed to spend the summer?!" Jenna scrunched up her face and glared at Max, who was sleepily leaning against the rear left window of her parents' tiny family car.

"Mmm..." he hummed.

"You're asleep!" she accused.

Max blinked groggily. "Yeah, we've been driving for almost five hours. What did you expect me to do?"

"I don't know, maybe take an interest in where we're going? Try to figure it out?"

"Why? Would it change anything?" he mumbled, closing his eyes.

"I don't know, maybe because it's important? Maybe because we're spending six weeks there? Maybe because this place is so insignificant it doesn’t even show up on the map?!"

"It'll be fine..." Max muttered and drifted back to sleep.

"Ugh!" Jenna groaned and turned her gaze back to the window. It was her first time leaving the big city, heading to the Midwest of the United States. The scenery gradually shifted from tightly packed skyscrapers to suburban homes and finally to isolated farmhouses and endless fields of farmland. Jenna didn’t like it. She felt secure among the concrete jungles of the city, where everything was close by, noise was constant, and people were always around. She couldn’t imagine what she'd do with all the quiet once they arrived.

Despite her determination to stay awake and understand where they were heading, the long drive eventually wore her out, and she fell asleep.

She woke up to the car stopping abruptly, with dust swirling around them. They had arrived. The place looked desolate. A small, shriveled woman stood in the doorway of an old farmhouse. Above her hung a battered wooden sign with faded letters reading, "Aunt Rose’s Pumpkin Farm." On the right side of the sign, there was a small illustration of a pumpkin.

"Come on, kids, we're here," Jenna's mom said cheerfully, but Jenna knew it was fake enthusiasm.

They unbuckled their seatbelts and stepped out. Aunt Rose came to greet them, inviting Jenna’s parents inside for coffee since they were the first to arrive. Jenna and Max stayed outside, listening to the muffled voices coming from inside.

Jenna sat on the creaky wooden steps, resting her chin in her hands, while Max leaned on the broken railing. They surveyed the area. Like every farm Jenna had seen in movies, this one was completely isolated, surrounded only by vast pumpkin fields and clusters of trees in the distance. The house itself looked ancient and weathered, with rotting wood beams and deep scratches, as if a tornado had torn through it. Max mentioned the scratches might be from flying debris during a storm, and Jenna nodded in agreement.

About forty yards from the house stood a barn with doors swaying slightly in the breeze. They assumed it stored farm equipment. There were no animals around, and Jenna thought of Mr. Whiskers, her fat and lazy cat, realizing how much she'd miss him.

"What a waste of a summer. We could've been at a camp right now, lounging on a boat at some lake... but no. We're here, in the middle of nowhere, harvesting pumpkins like mules," Max sighed.

"Yeah, it's really strange. This whole place feels like it popped up out of nowhere. And what's with Aunt Rose? Whose aunt is she, anyway? It seems like no one else lives here," Jenna fumed. "And what are we even supposed to do here, cut off from civilization? Look—" she held up her phone. "Barely any signal, let alone internet. It's inhumane."

"Yeah, it's annoying, but there’s not much we can do. At least some people we know from school are coming."

Jenna raised an eyebrow. "What? Who else is supposed to come?"

"I know Andy is coming, and maybe Michael Boone and Shirley too."

"Really?" For a moment, her anger subsided, and she felt a little better. "That’s nice."

"Yeah..." Max replied indifferently.

"Who even put this ridiculous idea in our parents’ heads?" Jenna was back to fuming.

"You missed it, I think. It happened the week you were sick," he recalled.

"What happened?"

Max furrowed his brow, trying to remember. "There was some meeting with the parents, and this group of overly cheerful weirdos showed up handing out flyers about 'Summer at Aunt Rose’s Farm.' They emphasized it was like camp, but they’d pay us because it’s work—learning the secrets of pumpkin harvesting or something like that..."

"Oh, right. I remember when my parents told me about it. It sounded so random. Really weird."

"Yeah, and somehow they agreed to it pretty quickly," he said bitterly.

Jenna sighed. "Honestly, I don’t think they had a choice, Maxie. They can’t really afford to send us to some camp or anything. You know that. I’m just daydreaming about those things."

"That’s nonsense. We could’ve stayed home and worked there. We didn’t have to cross half the country for this."

In the distance, they heard music approaching. "Hey! A car’s coming."

They turned toward the driveway. Loud music blared as a black van screeched to a halt near the house, enveloped in a cloud of dust. The side door slammed open, and a dark-haired teenager jumped out, slamming it shut behind him.

Someone inside the van turned down the music. "Cody! Call me after you settle in!" a male voice shouted from the front seat. Cody didn’t even glance back. He just glared at Jenna and Max, slung a black bag over his shoulder, and went to sit in the shade on a rusty plow. The van drove off, its music fading quickly, leaving silence behind.

"I can’t believe it!" Jenna moved closer to Max and whispered. "That’s Cody Walker! There are rumors about him at school that stretch all the way to Canada!"
"""


ref = 'rebecca' # kate_reading, amanda_leigh, ralph, rebecca
chunk_size = 350
audio_format = 'wav'

base = '/home/nim'

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

name = "Pumpkin"
chapter_folder = os.path.join(base, name)
os.makedirs(chapter_folder, exist_ok=True)


chapter_chunks = efficient_split_text_to_chunks(text, max_length=chunk_size)
chapter_chunks = [process_chunk_add_new_section(chunk) for chunk in chapter_chunks] # Pay attention here to the num of \n (especially for paragraphs
chapter_chunks = [process_chunk_replace_quotes_newline(chunk) for chunk in chapter_chunks] # There's also a function for newlines
chapter_chunks = [replace_newline_after_quote(chunk) for chunk in chapter_chunks]
chapter_chunks = [replace_right_quote_newline(chunk) for chunk in chapter_chunks]
chapter_chunks = [fix_punctuation_spacing(chunk) for chunk in chapter_chunks]


# Process each chunk and generate audio
for idx, chunk in enumerate(tqdm(chapter_chunks)):
    filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
    print(chunk)
    tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

    # if idx == 8:
    #     break

# Concat parts to assemble the chapter
# # Concat parts to assemble the chapter
output_file = chapter_folder  + '/'+ f"Sample.{audio_format}"  # Replace with your output file path
concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)


###################
def efficient_split_text_to_chunks2(text, max_length):
    """
    Splits the text into the largest possible chunks based on the assigned maximum length,
    ensuring each chunk ends at a sentence boundary ('.') when possible.
    If no '.' is found, then split by ','.
    If no ',' is found, splits at the nearest whitespace to avoid breaking words.

    Args:
        text (str): The input text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        # Determine the furthest point for the current chunk
        end = min(start + max_length, len(text))

        # Look for the last '.' within the allowable range
        last_dot_index = text.rfind(".", start, end)

        if last_dot_index == -1:  # If no '.' is found in the range
            # Look for the last ',' within the range
            last_comma_index = text.rfind(",", start, end)
            if last_comma_index != -1:  # If a ',' is found, split at the comma
                last_dot_index = last_comma_index
            else:  # If no ',' is found, look for the last whitespace
                last_space_index = text.rfind(" ", start, end)
                if last_space_index != -1:  # If a space is found, split at the space
                    last_dot_index = last_space_index
                else:  # If no space is found, split at the max length
                    last_dot_index = end

        # Add the chunk
        chunks.append(text[start:last_dot_index].strip())
        # Update the start to the new position
        start = last_dot_index + 1

    return [chunk for chunk in chunks if chunk]  # Remove any empty chunks

text = (
    "This is a long text. It contains multiple sentences, each separated by punctuation. "
    "If a period isn't found, the text should split at a comma, and if neither is present, it splits by spaces."
)

max_length = 150
chunks = efficient_split_text_to_chunks2(text, max_length)

for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}: {chunk}")