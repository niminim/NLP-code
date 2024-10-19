from TTS.api import TTS
import soundfile as sf

# 1. Initialize TTS model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(model_name)


# 2. Input text to convert to speech
# text = "Hello! This is a text-to-speech demonstration using a TTS model from Hugging Face."

text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan. Selling the shoes from the trunk of his lime green Plymouth Valiant,
Knight grossed $8,000 his first year. Today, Nike’s annual sales top $30 billion. In an age of startups, Nike is the ne plus ultra
of all startups, and the swoosh has become a revolutionary, globe-spanning icon, one of the most ubiquitous and recognizable
symbols in the world today.

"""

# But Knight, the man behind the swoosh, has always remained a mystery. Now, for the first time, in a memoir that is candid, humble,
# gutsy, and wry, he tells his story, beginning with his crossroads moment. At 24, after backpacking around the world, he decided
# to take the unconventional path, to start his own business—a business that would be dynamic, different.
#
# Knight details the many risks and daunting setbacks that stood between him and his dream—along with his early triumphs. Above all,
# he recalls the formative relationships with his first partners and employees, a ragtag group of misfits and seekers who became a
# tight-knit band of brothers. Together, harnessing the transcendent power of a shared mission, and a deep belief in the spirit of sport,
# they built a brand that changed everything.

# 3. Generate speech audio (numpy array)
audio = tts.tts(text)

# 4. Save the generated audio to a WAV file
filename = 'GR_book'
sf.write(f"//home/nim/venv/NLP-code/TTS/{filename}.wav", audio, samplerate=22050)
print(f"Audio generated and saved as {filename}.wav'")