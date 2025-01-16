import os
import json

import sys
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from TTS_code.audiobooks_studio.book_chapters import *
from TTS_code.audiobooks_studio.speech2text.compate_text_helper import *


# Find problems across all chapters
if __name__ == "__main__":

    ref = 'scott_brick'

    base = "/home/nim"
    book_name = 'To_Sleep_With_Evil'  # Lord_of_the_Necropolis

    book_path, json_dir, orig_chunks_dir, transcribed_dir = get_dirs(base, book_name, ref)
    chapters = chapter_names[book_name]  # chapters we want to subscribe
    chapters = ['Book']

    to_correct = {}

    for chapter in chapters:
        if chapter in os.listdir(os.path.join(transcribed_dir)):
            print(f"chapter: {chapter}")
        else:
            print(f"chapter: {chapter} - not in transcriptions")
            break

        orig_text_files = get_sorted_text_files(os.path.join(book_path, "texts", "orig_chunks", chapter))

        evaluation_data = {} # Initialize the data structure

        for part in np.arange(1,len(orig_text_files)+1):
            original = open_text_file(f"{book_path}/texts/orig_chunks/{chapter}/part{part}.txt")
            transcribed = open_text_file(f"{book_path}/texts/transcriptions/{chapter}/part{part}.txt")
            original_normalized, transcribed_normalized, wer, cer, len_diff = compare_texts(original, transcribed)

            json_file = f"{book_path}/texts/comparisons/{chapter}.json"
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            update_evaluation_data(evaluation_data, chapter, part, original_normalized, transcribed_normalized, wer, cer, len_diff)

            # define rules for plausible problematic parts
            if part != 1:
                if (cer * 100 > 6.0) or (abs(len_diff) >= 2):
                    print('part: ', part)
                    print(f"WER: {wer:.2%}")
                    print(f"CER: {cer:.2%}")
                    print(f"Diff (words): {len_diff}")
                    update_parts_to_correct(to_correct, chapter, part)
                    print('*******')

        # Save with or without indent
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(evaluation_data, file, indent=4)  # Use `indent=4` for pretty formatting or remove it for compact JSON
        print(f"JSON file saved at: {json_file}")
##############################



############################### Correction - Recreate all problematic chunks
from TTS_code.audiobooks_studio.tools.create_models import *
from TTS_code.audiobooks_studio.speech2text.STT_helper import *

tts_model = get_model(model_name ='xtts_v2')
model, processor = get_STT_model(model_name='whisper')

reps = 2

# Iterate through each chapter and its corresponding parts
for chapter, parts in to_correct.items():
    print(f"Chapter: {chapter}")
    for part in parts:
        chunk_text_path = os.path.join(orig_chunks_dir, chapter,f"part{part}.txt")
        chunk = open_text_file(chunk_text_path)

        for rep in np.arange(1,reps+1):
            print(rep)
            filepath = f"{base}/corrections_{book_name}/{chapter}/part{part}_{rep}.wav"
            os.makedirs(os.path.dirname(filepath),exist_ok=True)
            tts_model.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

    ######## Transcribe
    audio_dir = os.path.join(base,f"corrections_{book_name}", chapter)
    transcriptions_dir = audio_dir
    transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)
##############################



########### Choose best repetitions
for chapter in chapters:
    print(chapter)
    orig_json_path = os.path.join(json_dir, f"{chapter}.json")
    orig_chapter_stats = read_json_file(orig_json_path)[f"chapter {chapter}"]

    chapter_fix_dir = os.path.join(base,f"corrections_{book_name}", chapter)
    fix_part_nums = get_sorted_part_numbers(chapter_fix_dir)

    for part in fix_part_nums:
        fix_parts_stats = {}

        orig_part_stats = orig_chapter_stats[f"Part {part}"]
        original = open_text_file(f"{book_path}/texts/orig_chunks/{chapter}/part{part}.txt")

        fix_chapter_dir = os.path.join(base, f"corrections_{book_name}", chapter)
        fix_transcribed_paths = find_files_with_prefix_and_format(folder_path=fix_chapter_dir, prefix=f"part{part}", file_format=".txt")

        for rep_idx, transcribed_path in enumerate(fix_transcribed_paths):
            transcribed = open_text_file(transcribed_path)
            original_normalized, transcribed_normalized, wer, cer, len_diff = compare_texts(original, transcribed)
            fix_parts_stats[rep_idx+1] = {'WER': f"{wer:.2%}", 'CER': f"{cer:.2%}", 'len_diff': len_diff}

            print('part: ', part)
            print(f"WER: {wer:.2%}")
            print(f"CER: {cer:.2%}")
            print(f"Diff (words): {len_diff}")
            print('*******')

            if abs(len_diff)<abs(orig_part_stats['len_diff']):

                 cer = float(cer.strip('%'))
                 wer = float(wer.strip('%'))

























