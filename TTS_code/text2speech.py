import os
import torch
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from tqdm import tqdm

# Initialize the processor and model
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3").to("cuda")


def preprocess_audio(file_path):
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


def transcribe_audio_folder(chapter_folder):
    # Ensure the folder exists
    if not os.path.exists(chapter_folder):
        print(f"Folder not found: {chapter_folder}")
        return

    # List and sort .wav files numerically (e.g., part1, part2, ...)
    wav_files = sorted(
        [f for f in os.listdir(chapter_folder) if f.endswith('.wav')],
        key=lambda x: int(''.join(filter(str.isdigit, x)))
    )
    if not wav_files:
        print(f"No .wav files found in: {chapter_folder}")
        return

    # Create an output folder for transcriptions
    output_folder = os.path.join(chapter_folder, "transcriptions")
    os.makedirs(output_folder, exist_ok=True)

    # Loop through and transcribe each file

    for idx, wav_file in enumerate(tqdm(wav_files)):
    # for wav_file in wav_files:
        file_path = os.path.join(chapter_folder, wav_file)
        try:
            # Preprocess the audio file
            input_features = preprocess_audio(file_path).to("cuda")

            # Generate transcription
            predicted_ids = model.generate(input_features)
            transcribed_text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            # Show the transcribed text in the console
            print(f"\nTranscription for {wav_file}:\n{transcribed_text}\n")

            # Save transcription to a text file
            output_file = os.path.join(output_folder, f"{os.path.splitext(wav_file)[0]}.txt")
            with open(output_file, "w") as f:
                f.write(transcribed_text)

        except Exception as e:
            print(f"Error processing {wav_file}: {e}")


# Example usage
chapter_folder = "/home/nim/Baroness_of_Blood2_by_ralph_lister_350/One"
transcribe_audio_folder(chapter_folder)