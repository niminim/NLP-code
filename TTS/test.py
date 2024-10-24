from TTS.api import TTS
import soundfile as sf
import numpy as np
from scipy.signal import resample
import torch

# Initialize TTS model
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name).to(device)

# The provided text
text = """
In 1962, fresh out of business school, Phil Knight borrowed $50 from his father and created a company with a simple mission: import high-quality, low-cost athletic shoes from Japan. Selling the shoes from the trunk of his lime green Plymouth Valiant, Knight grossed $8,000 his first year. Today, Nike’s annual sales top $30 billion. In an age of startups, Nike is the ne plus ultra of all startups, and the swoosh has become a revolutionary, globe-spanning icon, one of the most ubiquitous and recognizable symbols in the world today.
But Knight, the man behind the swoosh, has always remained a mystery. Now, for the first time, in a memoir that is candid, humble, gutsy, and wry, he tells his story, beginning with his crossroads moment. At 24, after backpacking around the world, he decided to take the unconventional path, to start his own business—a business that would be dynamic, different.
Knight details the many risks and daunting setbacks that stood between him and his dream—along with his early triumphs. Above all, he recalls the formative relationships with his first partners and employees, a ragtag group of misfits and seekers who became a tight-knit band of brothers. Together, harnessing the transcendent power of a shared mission, and a deep belief in the spirit of sport, they built a brand that changed everything.
"""

def split_text(text, max_length=300):
    sentences = text.split('. ')
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def trim_silence(audio, threshold=1e-4):
    non_silent_indices = np.where(np.abs(audio) > threshold)[0]
    if len(non_silent_indices) == 0:
        return np.array([])  # Handle empty audio case
    return audio[non_silent_indices[0]:non_silent_indices[-1] + 1]

def generate_silence(duration, samplerate=22050):
    return np.zeros(int(duration * samplerate))

# Split text and generate audio
text_chunks = split_text(text, max_length=300)
audio_arrays = [trim_silence(tts.tts(chunk)) for chunk in text_chunks]

# Add silence between chunks to smooth transitions
silence = generate_silence(0.1)
combined_audio = np.concatenate([np.concatenate([a, silence]) for a in audio_arrays])

# Save combined audio
output_filename = 'GR_book_concat_chunks.wav'
sf.write(f"/home/nim/venv/NLP-code/TTS/{output_filename}", combined_audio, samplerate=22050)
print(f"Audio saved as {output_filename}")