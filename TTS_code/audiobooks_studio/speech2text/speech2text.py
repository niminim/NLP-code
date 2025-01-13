import os
import torch
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from tqdm import tqdm


def get_model(model_name):

    if model_name=='whisper':
        # Initialize the processor and model
        processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
        model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3").to("cuda")
    return model, processor


def preprocess_audio(processor, file_path):
    """
    Preprocess the audio file to extract features suitable for Whisper.
    """
    audio, sr = librosa.load(file_path, sr=16000)  # Load audio at 16 kHz
    input_features = processor.feature_extractor(
        audio,
        sampling_rate=sr,
        return_tensors="pt"
    ).input_features
    return input_features


def transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir):
    # Ensure the folder exists
    if not os.path.exists(audio_dir):
        print(f"Folder not found: {audio_dir}")
        return

    # List and sort .wav files numerically (e.g., part1, part2, ...)
    wav_files = sorted(
        [f for f in os.listdir(audio_dir) if f.endswith('.wav')],
        key=lambda x: int(''.join(filter(str.isdigit, x)))
    )
    if not wav_files:
        print(f"No .wav files found in: {audio_dir}")
        return

    # Create an output folder for transcriptions
    os.makedirs(transcriptions_dir, exist_ok=True)

    # Loop through and transcribe each file
    for idx, wav_file in enumerate(tqdm(wav_files)):
    # for wav_file in wav_files:
        file_path = os.path.join(audio_dir, wav_file)
        try:
            # Preprocess the audio file
            input_features = preprocess_audio(processor,file_path).to("cuda")

            # Generate transcription
            predicted_ids = model.generate(input_features)
            transcribed_text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            # Show the transcribed text in the console
            print(f"\nTranscription for {audio_dir.split('/')[-1]} - {wav_file}:\n{transcribed_text}\n")

            # Save transcription to a text file
            output_file = os.path.join(transcriptions_dir, f"{os.path.splitext(wav_file)[0]}.txt")
            with open(output_file, "w") as f:
                f.write(transcribed_text)

        except Exception as e:
            print(f"Error processing {wav_file}: {e}")


############################## One chapter

base = '/home/nim/'
book_name = 'Lord_of_the_Necropolis'
book_dir = f"{book_name}_by_scott_brick_100" # Baroness_of_Blood2_by_ralph_lister_350, King_of_the_Dead_by_scott_brick_350
# The_Dragons_of_Krynn_NEW5_by_ralph_lister_350, Forged_in_Cold_by_ralph_lister_350,
book_path = os.path.join(base, book_dir)

chapter = "One"  # Prologue, One
# chapter = "Scourge_of_the_Wicked_Kendragon"
chapter = "Preface"

model_name= 'whisper'
model, processor = get_model(model_name)

audio_dir = os.path.join(book_path, "audio", chapter)
transcriptions_dir = os.path.join(base, book_dir, "texts", "transcriptions", chapter)
transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)
#######################


###################### Multipile chapters
import os
import sys
project_root = os.path.abspath("/TTS_code")
sys.path.append(project_root)
from TTS_code.audiobooks_studio.book_chapters import *

base = '/home/nim/'
book_name = 'Lord_of_the_Necropolis'
book_dir = f"{book_name}_by_scott_brick_350"
book_path = os.path.join(base, book_dir)

chapters = chapter_names[book_name] # chapters we want to subscribe

model, processor = get_model(model_name='whisper')

for chapter_idx, chapter in enumerate(tqdm(chapters)):

    audio_dir = os.path.join(book_path, "audio", chapter)
    transcriptions_dir = os.path.join(base, book_dir, "texts", "transcriptions", chapter)
    transcribe_audio_folder(processor, model, audio_dir, transcriptions_dir)


