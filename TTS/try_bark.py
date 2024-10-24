from transformers import BarkModel, BarkProcessor

model = BarkModel.from_pretrained("suno/bark-small")
processor = BarkProcessor.from_pretrained("suno/bark-small")

# add a speaker embedding
inputs = processor("This is a test!", voice_preset="v2/en_speaker_3")

speech_output = model.generate(**inputs).cpu().numpy()

# try it in French, let's also add a French speaker embedding
inputs = processor("C'est un test!", voice_preset="v2/fr_speaker_1")

speech_output = model.generate(**inputs).cpu().numpy()

inputs = processor(
    "[clears throat] This is a test ... and I just took a long pause.",
    voice_preset="v2/fr_speaker_1",
)

speech_output = model.generate(**inputs).cpu().numpy()

inputs = processor(
    "♪ In the mighty jungle, I'm trying to generate barks.",
)

speech_output = model.generate(**inputs).cpu().numpy()


input_list = [
    "[clears throat] Hello uh ..., my dog is cute [laughter]",
    "Let's try generating speech, with Bark, a text-to-speech model",
    "♪ In the jungle, the mighty jungle, the lion barks tonight ♪",
]

# also add a speaker embedding
inputs = processor(input_list, voice_preset="v2/en_speaker_3")

speech_output = model.generate(**inputs).cpu().numpy()


import soundfile as sf
filename = 'GR_book_t5'
sf.write(f"//home/nim/venv/NLP-code/TTS/{0}.wav", speech_output[0], samplerate=22050)
sf.write(f"//home/nim/venv/NLP-code/TTS/{1}.wav", speech_output[1], samplerate=22050)
sf.write(f"//home/nim/venv/NLP-code/TTS/{2}.wav", speech_output[2], samplerate=22050)



