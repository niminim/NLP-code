import os
from tqdm import tqdm

import sys
project_root = os.path.abspath("/home/nim/venv/NLP-code/TTS_code/audiobooks_studio")
sys.path.append(project_root)

from tools.read_file import *
from tools.split_text import *
from tools.clean_text import *
from tools.finalize_files import *
from tools.text_tools import *
from tools.path_tools import *
from tools.create_models import *

import nltk
# nltk.download('punkt')

#############################################################################

from nltk.tokenize import sent_tokenize

def split_text_by_sentences_nltk(text):
    """
    Split the text into sentences using NLTK's sentence tokenizer.
    """
    sentences = sent_tokenize(text)
    return sentences


# Path to your EPUB file
file_path = '/home/nim/Downloads/Forged_In_Cold-Diane.epub'
file_path = '/home/nim/Downloads/Lord_of_the_Necropolis.epub'
epub_content = read_epub(file_path)

ref = 'scott_brick' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler, emilia_clarke, perdita_weeks, scott_brick,
chunk_size = 350
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1

base = '/home/nim'
book_name = 'Lord_of_the_Necropolis'
book_path, audio_dir, text_chunks_dir, text_transcriptions_dir = create_dirs(base, book_name, ref, chunk_size)

tts_model = get_model(model_name ='xtts_v2')

chapter_text = epub_content[-3100:-2100] # for Forged in cold  epub_content[:-283]
chapter_name = 'Preface'.replace(' ', '_')
chapter_audio_dir =  os.path.join(book_path, 'audio', chapter_name)
os.makedirs(chapter_audio_dir, exist_ok=True)

processed_substring = remove_first_newline_block(chapter_text[:50])
chapter_text = processed_substring + chapter_text[50:]
chapter_text = add_space_after_nth_newline_block(chapter_text, 1)
processed_substring = process_chunk_add_new_section(chapter_text[100:])
chapter_text = chapter_text[:100] + processed_substring
chapter_text = process_text(chapter_text) # pay attention to paragraphs newlines (currently supports one and two)
# chapter_chunks = split_text_by_sentences_nltk(chapter_text)
chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)

# Process each chunk and generate audio
for idx, chunk in enumerate(tqdm(chapter_chunks)):

    save_text_chunk(text_chunks_dir, chapter_name, chunk, idx)
    filepath = os.path.join(chapter_audio_dir, f"part{idx + 1}.wav")
    print(chunk)
    tts_model.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)


# Concat parts to assemble the chapter
chapter_str = chapter_idx_str(chapter_idx=0, start_zero=True)
output_file = os.path.join(audio_dir, chapter_str + chapter_name + f".{audio_format}")  # Replace with your output file path
concat_wavs_in_folder(chapter_audio_dir, output_file, format=audio_format)


####