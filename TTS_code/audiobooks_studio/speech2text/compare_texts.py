import os
import re
import numpy as np
import json

import sys
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from TTS_code.audiobooks_studio.book_chapters import *
from TTS_code.audiobooks_studio.speech2text.compate_text_helper import *


# Find problems
if __name__ == "__main__":

    base = "/home/nim"
    book_name = 'Lord_of_the_Necropolis'
    book_dir = f"{book_name}_by_scott_brick_350" # The_Dragons_of_Krynn_NEW5_by_ralph_lister_350

    chapter = 'One' # Prologue, Oneת Scourge_of_the_Wicked_Kendragon
    part = '32'

    book_path = os.path.join(base, book_dir)
    json_dir = os.path.join(book_path, "texts", "comparisons")
    os.makedirs(json_dir, exist_ok=True)
    orig_chunks_dir = f"{book_path}/texts/orig_chunks"
    transcribed_dir = f"{book_path}/texts/transcriptions"

    chapters = chapter_names[book_name]  # chapters we want to subscribe

    to_correct = {}

    for chapter in chapters:
        if chapter in os.listdir(os.path.join(transcribed_dir)):
            print(f"chapter: {chapter}")
        else:
            print(f"chapter: {chapter} - not in transcriptions")
            break

        orig_text_files = get_sorted_text_files(os.path.join(book_path, "texts", "orig_chunks", chapter))

        # Initialize the data structure
        evaluation_data = {}

        for part in np.arange(1,len(orig_text_files)+1):
            original = open_text_file(f"{book_path}/texts/orig_chunks/{chapter}/part{part}.txt")
            transcribed = open_text_file(f"{book_path}/texts/transcriptions/{chapter}/part{part}.txt")
            original_normalized, transcribed_normalized, wer, cer, len_diff = compare_texts(original, transcribed)

            json_file = f"{book_path}/texts/comparisons/{chapter}.json"
            os.makedirs(os.path.dirname(json_file), exist_ok=True)

            if part != 1:
                if (cer * 100 > 6.0) or (len_diff >= 2):
                    print('part: ', part)
                    print(f"WER: {wer:.2%}")
                    print(f"CER: {cer:.2%}")
                    print(f"Diff (words): {len_diff}")
                    update_parts_to_correct(to_correct, chapter, part)
                    print('*******')

            update_evaluation_data(evaluation_data, chapter, part, original_normalized, transcribed_normalized, wer, cer)

        # Save with or without indent
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(evaluation_data, file, indent=4)  # Use `indent=4` for pretty formatting or remove it for compact JSON
        print(f"JSON file saved at: {json_file}")




############################### Correction - Recreate all problematic chunks
from TTS_code.audiobooks_studio.tools.create_models import *
from TTS_code.audiobooks_studio.speech2text.STT_helper import *

tts_model = get_model(model_name ='xtts_v2')
model, processor = get_STT_model(model_name='whisper')


ref = 'scott_brick'

# Iterate through each chapter and its corresponding parts
for chapter, parts in to_correct.items():
    print(f"Chapter: {chapter}")
    for part in parts:
        print(f"  Part: {part}")

        chunk_text_path = os.path.join(orig_chunks_dir, chapter,f"part{part}.txt")
        chunk = open_text_file(chunk_text_path)


        filepath = f"{base}/corrections/{chapter}/part{part}.wav"
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        tts_model.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)


        ######## Transcribe
        audio_dir = os.path.join(base,"corrections", chapter)
        transcriptions_dir = audio_dir
        transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)









