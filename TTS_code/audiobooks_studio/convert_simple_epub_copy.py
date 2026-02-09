import os
from tqdm import tqdm
import time

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

epub_content = read_epub(file_path)

ref = 'scott_brick' # kate_reading, amanda_leigh_cobb, ralph_lister, rebecca_soler, emilia_clarke, perdita_weeks, scott_brick,
chunk_size = 250
audio_format = 'wav'
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1

base = '/home/nim'
book_name = 'Forged_In_Cold'
book_path, audio_dir, text_chunks_dir, text_transcriptions_dir = create_dirs(base, book_name, ref, chunk_size)


import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import torchaudio as ta

# English example
tts_model = ChatterboxTTS.from_pretrained(device="cuda")

chapter_text = epub_content[:-283] # for Forged in cold  epub_content[:-283]

chapter_name = 'Book'.replace(' ', '_')
chapter_audio_dir =  os.path.join(book_path, 'audio', chapter_name)
os.makedirs(chapter_audio_dir, exist_ok=True)

processed_substring = remove_first_newline_block(chapter_text[:50])
chapter_text = processed_substring + chapter_text[50:]
chapter_text = add_space_after_nth_newline_block(chapter_text, 1)
processed_substring = process_chunk_add_new_section(chapter_text[100:], size=2)
chapter_text = chapter_text[:100] + processed_substring
chapter_text = process_text(chapter_text) # pay attention to paragraphs newlines (currently supports one and two)
# chapter_chunks = split_text_by_sentences_nltk(chapter_text)
chapter_chunks = split_text_into_chunks(chapter_text, max_chunk=chunk_size)

AUDIO_PROMPT_PATH = "/home/nim/Downloads/UG.wav"

# Process each chunk and generate audio
for idx, chunk in enumerate(tqdm(chapter_chunks)):

    save_text_chunk(text_chunks_dir, chapter_name, chunk, idx)
    filepath = os.path.join(chapter_audio_dir, f"part{idx + 1}.wav")
    print(chunk)

    # If you want to synthesize with a different voice, specify the audio prompt
    wav = tts_model.generate(chunk, audio_prompt_path=f"/home/nim/Documents/{ref}.wav")
    ta.save(filepath, wav, tts_model.sr)

    # if idx == 20:
    #     break
    if idx % 150 == 0 and idx != 0:  # Check if the index is a multiple of 100
        time.sleep(15)

# Concat parts to assemble the chapter
chapter_str = chapter_idx_str(chapter_idx=0, start_zero=True)
output_file = os.path.join(audio_dir, chapter_str + chapter_name + f".{audio_format}")  # Replace with your output file path
concat_wavs_in_folder(chapter_audio_dir, output_file, format=audio_format)








########### To deal with to sleep with evil

# Assuming epub_content contains the text
text = epub_content[3900:-283]

# Results to store changes for each occurrence
results = []

# Function to replace \n blocks with chapter labels and capture results
def replace_with_chapter(match):
    global chapter_counter
    start, end = match.start(), match.end()  # Match start and end positions
    if chapter_counter == 0:
        replacement = ' Prologue '  # The first block is the prologue
    elif chapter_counter == 20:
        replacement = ' Epilogue '  # The last block is the epilogue
    else:
        replacement = f' Chapter {chapter_counter} '  # Subsequent blocks are numbered chapters
    chapter_counter += 1

    # Capture the replacement and 20 characters after the replacement
    snippet_start = start  # Start from where the \n block started
    snippet_end = min(len(text), end + len(replacement) + 20)  # 20 chars after the replacement
    snippet = text[snippet_start:snippet_end].replace("\n", "\\n")  # For better readability

    # Store the result
    results.append((start, replacement, snippet))
    return replacement

# Initialize a counter to track the chapter number
chapter_counter = 0

# Replace blocks of more than 5 newlines with the respective labels
updated_text = re.sub(r'(?:\n){5,}', replace_with_chapter, text)

# Display results
for start, replacement, snippet in results:
    print(f"Replaced block starting at {start} with -> {replacement}")
    print(f"Snippet: {snippet}\n")

chapter_text = updated_text