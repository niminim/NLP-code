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
from tools.clean_text2 import *
from tools.finalize_files import *
from tools.text_tools import *
from tools.path_tools import *
from tools.general_tools import *



#############################################################################

# Path to your EPUB file
file_path = '/home/nim/Downloads/The_Dragons_of_Krynn.epub'
epub_content = read_epub(file_path)


ref = 'ralph_lister' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler
chunk_size = 350
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1


base = '/home/nim'
book_name = 'The_Dragons_of_Krynn_NEW4'
book_path, text_chunks_dir, text_transcriptions_dir = create_dirs(base, book_name, ref, chunk_size)

# List of chapters to find
chapters = ['Seven Hymns of the Dragon', 'The Final Touch', 'Night of Falling Stars', 'Honor Is All', 'Easy Pickings', 'A Dragon to the Core',
            'Dragon Breath', "Fool's Gold", 'Scourge of the Wicked Kendragon', 'And Baby Makes Three',
            'The First Dragonarmy Bridging Company', 'The Middle of Nowhere', "Kaz and the Dragon's Children",
            "Into the Light", "The Best", "The Hunt"]


# Find all locations of chapter titles
chapter_locations = find_chapter_locations_full_block(epub_content, chapters) # different here
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)



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

    processed_substring = remove_first_newline_block(chapter_text[:50])
    chapter_text = processed_substring + chapter_text[50:]
    chapter_text = add_space_after_nth_newline_block(chapter_text, 1)
    processed_substring = process_chunk_add_new_section(chapter_text[100:])
    chapter_text = chapter_text[:100] + processed_substring
    chapter_text = process_text(chapter_text) # pay attention to paragraphs newlines (currently su
    chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)


    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter idx {chapter_idx} - Processing chunks")):
        save_text_chunk(text_chunks_dir, chapter_name_adj, chunk, idx)

        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        # if idx == 38:
        #     break


    # # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(book_path, chapter_str + chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)

    # Sleep for 20 seconds
    time.sleep(20)
