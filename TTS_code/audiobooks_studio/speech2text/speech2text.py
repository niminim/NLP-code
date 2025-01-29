
###################### Multipile chapters
import os
import sys
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from TTS_code.audiobooks_studio.book_chapters import *
from TTS_code.audiobooks_studio.speech2text.STT_helper import *

base = '/home/nim/'
book_name = 'Shadowborn'
book_dir = f"{book_name}_by_scott_brick_250"
book_path = os.path.join(base, book_dir)

chapters = chapter_names[book_name] # chapters we want to subscribe

model, processor = get_STT_model(model_name='whisper')

for chapter_idx, chapter in enumerate(tqdm(chapters)):

    audio_dir = os.path.join(book_path, "audio", chapter)
    transcriptions_dir = os.path.join(base, book_dir, "texts", "transcriptions", chapter)
    transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)



############################## One chapter

base = '/home/nim/'
book_name = 'Shadowborn'
book_dir = f"{book_name}_by_scott_brick_250" # Baroness_of_Blood2_by_ralph_lister_350, King_of_the_Dead_by_scott_brick_350
# The_Dragons_of_Krynn_NEW5, Forged_in_Cold, To_Sleep_With_Evil, Shadowborn
book_path = os.path.join(base, book_dir)

chapter = "One"  # Prologue, One
# chapter = "Scourge_of_the_Wicked_Kendragon"
chapter = "Book"
chapter = "Twenty-three"

model_name= 'whisper'
model, processor = get_STT_model(model_name)

audio_dir = os.path.join(book_path, "audio", chapter)
transcriptions_dir = os.path.join(base, book_dir, "texts", "transcriptions", chapter)
transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)
#######################