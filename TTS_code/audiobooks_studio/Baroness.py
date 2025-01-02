import os
import time
from tqdm import tqdm

import torch
from TTS.api import TTS

import sys
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS_code/audiobooks_studio")
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
###### End of Chapter_start


#############################################################################


# Path to your EPUB file
file_path = '/home/nim/Downloads/Baroness_of_Blood.epub'
epub_content = read_epub(file_path)


# Print a portion of the EPUB content
# print(epub_content[8000:10000])  # Print the first 1000 characters

ref = 'rebecca_soler' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler, emilia_clarke, perdita_weeks, michael_page, scott_brick, john_lee2
chunk_size = 350
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1

base = '/home/nim'
book_name = 'Baroness_of_Blood' + f"_by_{ref}_{chunk_size}"
book_path = os.path.join(base, book_name)


# List of chapters to find
chapters = ['Prologue', 'One', 'Two', 'Three', 'Four','Five', 'Six', 'Seven','Eight', 'Nine','Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
            'Fifteen','Sixteen', 'Seventeen', 'Eighteen', 'Nineteen','Twenty', 'Twenty-one', 'Twenty-two', 'Twenty-three',
            'Twenty-four', 'Twenty-five', 'Twenty-six', 'Twenty-seven','Twenty-eight', 'Twenty-nine', 'Thirty', 'Thirty-one','Epilogue',
            'Back Cover', 'About the Author'] # Parts appears at the end! only used as a stop point


# Find all locations of chapter titles
chapter_locations = find_chapter_locations_full_block2(epub_content, chapters) # different here
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)


device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

for chapter_idx in [0]:
    chapter_text, chapter_info = get_chapter_text(epub_content, chapters_dict, chapters, chapter_idx)
    chapter_name = chapters[chapter_idx]
    chapter_name_adj = chapter_name.replace(' ', '_')
    chapter_folder =  os.path.join(book_path, chapter_name_adj)
    os.makedirs(chapter_folder, exist_ok=True)


    chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)
    chapter_chunks[0] = add_space_after_first_newline_block(chapter_chunks[0])
    chapter_chunks[1:] = [process_chunk_add_new_section(chunk) for chunk in chapter_chunks[1:]] # Pay attention here to the num of \n (especially for paragraphs

    chapter_chunks[1:] = [fix_punctuation_with_quote(chunk) for chunk in chapter_chunks[1:]]
    chapter_chunks[1:] = [process_chunk_replace_quotes_newline(chunk) for chunk in chapter_chunks[1:]] # There's also a function for newlines
    chapter_chunks[1:] = [replace_newline_after_quote(chunk) for chunk in chapter_chunks[1:]]
    chapter_chunks[1:] = [replace_right_quote_newline(chunk) for chunk in chapter_chunks[1:]]


    if chapter_idx != 0 and chapter_idx != len(chapters)-3 and chapter_idx != len(chapters)-1: # last is used only as a stop point
        chapter_chunks[0] = 'Chapter ' + chapter_chunks[0] # The word Chapter should be added


    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter idx {chapter_idx} - Processing chunks")):
        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        # if idx == 8:
        #     break

    # Concat parts to assemble the chapter
    # # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(book_path, chapter_str + chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)

    # Sleep for 15 seconds
    time.sleep(5)

####