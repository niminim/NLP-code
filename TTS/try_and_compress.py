from TTS.api import TTS
import soundfile as sf
import subprocess

# Initialize TTS model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"

tts = TTS(model_name)

# The provided text (shortened for demonstration)
text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission:
import high-quality, low-cost athletic shoes from Japan. Selling the shoes from the trunk of his lime green Plymouth Valiant,
Knight grossed $8,000 his first year. Today, Nike’s annual sales top $30 billion. In an age of startups, Nike is the ne plus ultra
of all startups, and the swoosh has become a revolutionary, globe-spanning icon, one of the most ubiquitous and recognizable
symbols in the world today.

But Knight, the man behind the swoosh, has always remained a mystery. Now, for the first time, in a memoir that is candid, humble,
gutsy, and wry, he tells his story, beginning with his crossroads moment. At 24, after backpacking around the world, he decided
to take the unconventional path, to start his own business—a business that would be dynamic, different.

Knight details the many risks and daunting setbacks that stood between him and his dream—along with his early triumphs. Above all,
he recalls the formative relationships with his first partners and employees, a ragtag group of misfits and seekers who became a
tight-knit band of brothers. Together, harnessing the transcendent power of a shared mission, and a deep belief in the spirit of sport,
they built a brand that changed everything.
"""

# Generate the audio as a numpy array
audio = tts.tts(text)

# Save the audio as a WAV file (temporary)
temp_wav_file = "temp_GR_book_long.wav"
sf.write(f"//home/nim/venv/NLP-code/TTS/{temp_wav_file}", audio, samplerate=22050)  # Use 16kHz for smaller size

# Compress the WAV to MP3 using FFmpeg
output_mp3_file = "GR_book_long_mp3.mp3"
bitrate = "64k"  # Adjust bitrate for desired quality and size
subprocess.run([
    "ffmpeg", "-y", "-i", temp_wav_file,  # Input temporary WAV file
    "-ac", "1",                           # Convert to mono
    "-b:a", bitrate,                      # Set bitrate
    f"//home/nim/venv/NLP-code/TTS/{output_mp3_file}"                       # Output MP3 file
])

print(f"Compressed audio saved as '{output_mp3_file}'")