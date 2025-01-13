from transformers import pipeline
import soundfile as sf



# Load audio file and resample if necessary
file_path = "/home/nim/Baroness_of_Blood2_by_ralph_lister_350/audio/One/part2.wav"
audio_data, sample_rate = sf.read(file_path)

# If the sample rate is not 16000, resample it
if sample_rate != 16000:
    import librosa
    audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)


# Load the Whisper speech-to-text pipeline
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-medium")


result = stt_pipeline(audio_data)
print("Transcription:", result['text'])

