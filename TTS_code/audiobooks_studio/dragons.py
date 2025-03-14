import os
import time
from tqdm import tqdm

import sys
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS_code/audiobooks_studio")
sys.path.append(project_root)

from tools.read_file import *
from tools.locate_chapters import *
from tools.split_text import *
from tools.clean_text import *
from tools.finalize_files import *
from tools.text_tools import *
from tools.path_tools import *
from tools.text_conversion_tools import *
from tools.create_models import *
from book_chapters import *

#############################################################################

# Path to your EPUB file
file_path = '/home/nim/Downloads/The_Dragons_of_Krynn.epub'
epub_content = read_epub(file_path)


ref = 'scott_brick' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler
chunk_size = 250
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1


base = '/home/nim'
book_name = 'The_Dragons_of_Krynn'
book_path, audio_dir, text_chunks_dir, text_transcriptions_dir = create_dirs(base, book_name, ref, chunk_size)

# List of chapters to find
chapters = chapter_names['The_Dragons_of_Krynn']


# Find locations of chapters by their header
chapter_locations = find_chapter_locations_full_block(epub_content, chapters) # different here
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)

tts_model = get_model(model_name ='xtts_v2')


for chapter_idx in [8]:

    chapter_text, chapter_info = get_chapter_text(epub_content, chapters_dict, chapters, chapter_idx)
    chapter_name = chapters[chapter_idx].replace(' ', '_')
    chapter_audio_dir =  os.path.join(audio_dir, chapter_name)
    os.makedirs(chapter_audio_dir, exist_ok=True)

    if chapter_idx == 0:
        chapter_text = convert_latin_numbers_to_words(chapter_text)

    # Process each chunk
    processed_substring = remove_first_newline_block(chapter_text[:50])
    chapter_text = processed_substring + chapter_text[50:]
    chapter_text = add_space_after_nth_newline_block(chapter_text, 1)
    processed_substring = process_chunk_add_new_section(chapter_text[100:], size=4)
    chapter_text = chapter_text[:100] + processed_substring
    chapter_text = process_text(chapter_text) # pay attention to paragraphs newlines (currently su
    chapter_chunks = split_text_into_chunks(chapter_text, max_chunk=chunk_size)


    # Generate audio and save the original text of each chunk
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter idx {chapter_idx} - Processing chunks")):
        save_text_chunk(text_chunks_dir, chapter_name, chunk, idx)

        filepath = os.path.join(chapter_audio_dir, f"part{idx + 1}.wav")
        print(chunk)
        tts_model.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        if idx == 1:
            break

    # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(audio_dir, chapter_str + chapter_name + f".{audio_format}")
    concat_wavs_in_folder(chapter_audio_dir, output_file, format=audio_format)

    # Sleep for 10 seconds
    time.sleep(10)
