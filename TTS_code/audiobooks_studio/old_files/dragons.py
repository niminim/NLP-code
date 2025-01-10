import os
import time
from tqdm import tqdm

import torch
from TTS.api import TTS

import sys
project_root = os.path.abspath("/TTS_code/audiobooks_studio")
sys.path.append(project_root)

from tools.read_file import *
from tools.locate_chapters import *
from tools.split_text import *
from tools.clean_text import *
from tools.finalize_files import *


###### Chapter_start
def convert_latin_numbers_to_words(text):
    """
    Converts Latin numerals (I. to X.) into their word equivalents followed by '-'.
    Does nothing for Latin numerals without a '.'.

    Args:
        text (str): Input text containing Latin numerals.

    Returns:
        str: Text with Latin numerals followed by '.' replaced by words followed by '-'.
    """
    # Mapping of Latin numerals (with '.') to their word equivalents
    latin_to_words = {
        '\nI.': ' One -', '\nII.': ' Two -', '\nIII.': ' Three -', '\nIV.': ' Four -',
        '\nV.': ' Five -', '\nVI.': ' Six -', '\nVII.': ' Seven -', '\nVIII.': ' Eight -',
        '\nIX.': ' Nine -', '\nX.': ' Ten -'
    }

    # Replace numerals followed by '.' with their word equivalents
    for numeral, word in latin_to_words.items():
        text = text.replace(numeral, word)

    return text

# to deal with ' wire.\n\n\n\n\n\n\n\nScourge of the Wicked Kendragon\nJanet Pack\n\n\n\n\n\n\n"But I '
# (here, it's best to keep it)
def keep_n_sequences_with_position(input_text, n):
    """
    Keeps the first n newline sequences intact, replaces the rest with spaces,
    and returns the ending position of the nth sequence.

    Parameters:
    - input_text (str): The input text to process.
    - n (int): The number of newline sequences to retain.

    Returns:
    - tuple: (processed_text, end_position_of_nth_sequence)
    """
    # Split the input text into sequences based on newlines
    sequences = re.split(r'(\n+)', input_text)

    # Calculate the indices to retain
    retain_indices = 2 * n - 1  # Each sequence has a preceding text and newline part

    # Join retained parts
    retained_part = ''.join(sequences[:retain_indices + 1])

    # Replace the rest with spaces
    replaced_part = ''.join(sequences[retain_indices + 1:]).replace('\n', ' ')

    # Combine both parts
    processed_text = retained_part + replaced_part

    # Calculate the ending position of the nth newline sequence
    nth_sequence_text = ''.join(sequences[:retain_indices + 1])
    end_position_of_nth_sequence = len(nth_sequence_text)

    return processed_text, end_position_of_nth_sequence


def keep_n_sequences(input_text, n=2):
    processed_text, end_position_of_nth_sequence = keep_n_sequences_with_position(input_text, n=2)

    # Modify the text from the nth sequence onward
    # Here, we apply `clean_newline` to the portion after the nth sequence
    chunk_to_modify = processed_text[end_position_of_nth_sequence:]
    modified_chunk = ''.join([process_chunk_replace_quotes_newline(chunk) for chunk in chunk_to_modify])
    final_text = processed_text[:end_position_of_nth_sequence] + modified_chunk

    return final_text

def add_newline_after_chapter_name(text, chapter_name):
    """
    Adds a newline after the chapter name if it appears at the beginning of the text.

    Args:
        text (str): The input text.
        chapter_name (str): The chapter name to check and replace (default is "Scourge of the Wicked Kendragon").

    Returns:
        str: The modified text with a newline added after the chapter name.
    """
    if text.startswith(chapter_name):
        return text.replace(chapter_name, chapter_name + '\n', 1)
    return text
###### End of Chapter_start


#############################################################################

# Path to your EPUB file
file_path = '/home/nim/Downloads/The_Dragons_of_Krynn.epub'
epub_content = read_epub(file_path)


# Print a portion of the EPUB content
# print(epub_content[8000:10000])  # Print the first 1000 characters

ref = 'ralph_lister' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler
chunk_size = 350
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1


base = '/home/nim'
book_name = 'The_Dragons_of_Krynn_NEW3' + f"_by_{ref}_{chunk_size}"
book_path = os.path.join(base, book_name)


# List of chapters to find
chapters = ['Seven Hymns of the Dragon', 'The Final Touch', 'Night of Falling Stars', 'Honor Is All', 'Easy Pickings', 'A Dragon to the Core',
            'Dragon Breath', "Fool's Gold", 'Scourge of the Wicked Kendragon', 'And Baby Makes Three',
            'The First Dragonarmy Bridging Company', 'The Middle of Nowhere', "Kaz and the Dragon's Children",
            "Into the Light", "The Best", "The Hunt"]


# Find all locations of chapter titles
chapter_locations = find_chapter_locations_full_block(epub_content, chapters) # different here
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)


# # Print the chapter locations
# for chapter, locations in chapter_locations.items():
#     print(f"'{chapter}' found at positions: {locations}")


device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# for chapter_idx in [1,2,3,4,5,6,7,10,11,12,13,14]:
for chapter_idx in [8]:

    chapter_text, chapter_info = get_chapter_text(epub_content, chapters_dict, chapters, chapter_idx)

    chapter_name = chapters[chapter_idx]
    chapter_name_adj = chapter_name.replace(' ', '_')
    chapter_folder =  os.path.join(book_path, chapter_name_adj)
    os.makedirs(chapter_folder, exist_ok=True)

    if chapter_idx == 0:
        chapter_text = convert_latin_numbers_to_words(chapter_text)

    chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)
    chapter_chunks[0] = add_space_after_first_newline_block(chapter_chunks[0])
    chapter_chunks[1:] = [process_chunk_add_new_section(chunk) for chunk in chapter_chunks[1:]] # Pay attention here to the num of \n (especially for paragraphs
    chapter_chunks[1:] = [process_chunk_replace_quotes_newline(chunk) for chunk in chapter_chunks[1:]] # There's also a function for newlines
    chapter_chunks[1:] = [replace_newline_after_quote(chunk) for chunk in chapter_chunks[1:]]
    chapter_chunks[1:] = [replace_right_quote_newline(chunk) for chunk in chapter_chunks[1:]]
    chapter_chunks[1:] = [fix_punctuation_with_qoute(chunk) for chunk in chapter_chunks[1:]]

    # Deal with the header
    chapter_chunks[0] = keep_n_sequences(chapter_chunks[0], n=2)
    # chapter_chunks[0] = add_newline_after_chapter_name(chapter_chunks[0], chapter_name)


    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter idx {chapter_idx} - Processing chunks")):
        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        if idx == 38:
            break


    # # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(book_path, chapter_str + chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)

    # Sleep for 20 seconds
    time.sleep(20)

    ### IT STILL RUNS IN NEW 3  !!!!
