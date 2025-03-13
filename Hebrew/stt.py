import faster_whisper
model = faster_whisper.WhisperModel('ivrit-ai/whisper-large-v3-turbo-ct2')

file = '/home/nim/Downloads/eylon.wav'
file = '/home/nim/Downloads/eynat.wav'

segs, _ = model.transcribe(file, language='he')

texts = [s.text for s in segs]

transcribed_text = ' '.join(texts)
print(f'Transcribed text: {transcribed_text}')