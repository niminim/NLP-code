import os

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

    to_correct = {} # includes the parts to correct (of each chapter)

    for chapter in chapters:
        if chapter in os.listdir(os.path.join(transcribed_dir)):
            print(f"chapter: {chapter}")
        else:
            print(f"chapter: {chapter} - not in transcriptions")
            break

        # get the ordered (parts) transcription texts files
        orig_text_files = get_sorted_text_files(os.path.join(book_path, "texts", "orig_chunks", chapter))

        evaluation_data = {} # Initialize the data structure

        for part in np.arange(1,len(orig_text_files)+1):
            original = open_text_file(f"{book_path}/texts/orig_chunks/{chapter}/part{part}.txt")
            transcribed = open_text_file(f"{book_path}/texts/transcriptions/{chapter}/part{part}.txt")
            compare_texts_res = compare_texts(original, transcribed)


            json_file = f"{book_path}/texts/comparisons/{chapter}.json"
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            update_evaluation_data(evaluation_data, chapter, part, compare_texts_res)

            # define rules for plausible problematic parts
            if part != 1:
                if (compare_texts_res['CER'] * 100 > 6.0) or (abs(compare_texts_res['len_diff']) >= 2):
                    print('part: ', part)
                    print(f"WER: {compare_texts_res['WER']:.2%}")
                    print(f"CER: {compare_texts_res['CER']:.2%}")
                    print(f"Diff (words): {compare_texts_res['len_diff']}")
                    update_parts_to_correct(to_correct, chapter, part) # add the part to "to_correct" dict
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

reps = 3 # number of repetitions

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
fix_chapters_stats = {} # here we store the suspected parts, and add to that the replaced parts

for chapter in chapters:
    print(chapter)

    fix_chapters_stats[chapter] = {}
    orig_json_path = os.path.join(json_dir, f"{chapter}.json")
    orig_chapter_stats = read_json_file(orig_json_path)[f"chapter {chapter}"]
    fix_chapter_stats = {} # here we store the suspected parts (from all chapters), and add to that the replaced parts
    fix_chapters_stats[chapter] = {} # for a specif chapter (here we store all the relevant data to suspected parts)


    chapter_fix_dir = os.path.join(base,f"corrections_{book_name}", chapter)
    fix_part_nums = get_sorted_part_numbers(chapter_fix_dir)


    for part in fix_part_nums:
        fix_chapters_stats[chapter][part] = {}

        orig_part_stats = orig_chapter_stats[f"Part {part}"]
        original_chunk_norm = orig_part_stats['original_text']
        orig_transcribed_nom = orig_part_stats['transcribed_text']

        fix_chapter_dir = os.path.join(base, f"corrections_{book_name}", chapter)
        fix_transcribed_paths = find_files_with_prefix_and_format(folder_path=fix_chapter_dir, prefix=f"part{part}", file_format=".txt")

        # Collect data for the table
        stats_table = []

        for rep_idx, fix_transcribed_path in enumerate(fix_transcribed_paths):
            fix_chapters_stats[chapter][part][rep_idx+1] = {}

            fixed_transcribed = open_text_file(fix_transcribed_path)
            fix_compare_texts_res = compare_texts(original_chunk_norm, fixed_transcribed)
            update_fix_chapters_stats(fix_chapters_stats, chapter, part, rep_idx, fix_compare_texts_res, orig_part_stats)

            # Add row to the table
            update_fixed_stats_table(stats_table, rep_idx, fix_compare_texts_res)

            print(f"part: {part}, rep: {rep_idx+1}" )
            print(f"WER: {fix_compare_texts_res['WER']:.2%}")
            print(f"CER: {fix_compare_texts_res['CER']:.2%}")
            print(f"Diff (words): {fix_compare_texts_res['len_diff']}")


            # Use raw `wer` and `cer` variables for comparison
            if abs(fix_compare_texts_res['len_diff']) < abs(orig_part_stats['len_diff']):
                print(f"Improvement")
            print('***')
        sort_stats_table(fix_chapters_stats, stats_table, chapter, part)

        print('******')
    save_fix_chapters_stats_json(fix_chapters_stats, chapter_fix_dir)































