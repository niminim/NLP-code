from TTS.api import TTS
import soundfile as sf

# Initialize TTS model from Hugging Face Hub
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(model_name)

# The provided text
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


# Function to split text into manageable chunks if necessary
def split_text(text, max_length=300):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


# Split text if it's too long for one go
text_chunks = split_text(text, max_length=300)

# Process each chunk with TTS and save to separate audio files
for idx, chunk in enumerate(text_chunks):
    # Generate speech audio for each chunk
    audio = tts.tts(chunk)

    # Save each chunk to a separate WAV file
    output_filename = f"output_audio_chunk_{idx + 1}.wav"
    sf.write(f"//home/nim/venv/NLP-code/TTS/{output_filename}", audio, samplerate=22050)
    print(f"Audio generated and saved as '{output_filename}' for chunk {idx + 1}.")