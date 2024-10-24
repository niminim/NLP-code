# https://docs.coqui.ai/en/latest/inference.html

import torch
from TTS.api import TTS
import soundfile as sf
import numpy as np

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
# device = "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


text = """
PROLOGUE

Wayne knew about beds. Other kids in Tinweight Settlement had them. A bed sounded much better than a mat on the ground—especially one he had to share with his ma when the nights were cold, because they didn’t have any coal.

Plus there were monsters under beds.
Yeah, he’d heard stories of mistwraiths. They’d hide unner your bed and steal the faces of people you knew. Which made beds soft and squishy on top, with someone underneath you could talk to. Sounded like rustin’ heaven.

Other kids were scared of mistwraiths, but Wayne figured they just didn’t know how to negotiate properly. He could make friends with something what lived unner a bed. You just had to give it something it wanted, like someone else to eat.

Anyway, no bed for him. And no proper chairs. They had a table, built by Uncle Gregr. Back before he got crushed by a billion rocks in a landslide and mushed into a pulp what couldn’t hit people no more. Wayne kicked the table sometimes, in case Gregr’s spirit was watching and was fond of it. Rusts knew there was nothing else in this one-window home Uncle Gregr had cared about.

Best Wayne had was a stool, so he sat on that and played with his cards—dealing hands and hiding cards up his sleeve—as he waited. This was a nervous time of day. Every evening he feared she wouldn’t come home. Not because she didn’t love him. Ma was a burst of sweet spring flowers in a sewage pit of a world. But because one day Pa hadn’t come home. One day Uncle Gregr—Wayne kicked the table—hadn’t come home. So Ma . . .

Don’t think about it, Wayne thought, bungling his shuffle and spilling cards over the table and floor. And don’t look. Not until you see the light.

He could feel the mine out there; nobody wanted to live nexta it, so Wayne and his ma had to.

He thought of something else, on purpose. The pile of laundry by the wall that he’d finished washing earlier. That had been Ma’s old job what didn’t pay well enough. Now he did it while she pushed minecarts.

Wayne didn’t mind the work. Got to try on all the different clothes—whether they were from old gramps or young women—and pretend to be them. His ma had caught him a few times and grown angry. Her exasperation still baffled him. Why wouldn’t you try them on? That’s what clothes was for. It wasn’t nothing weird.

Besides, sometimes folks left stuff in their pockets. Like decks of cards.

He fumbled the shuffle again, and as he gathered the cards up he did not look out the window, even though he could feel the mine. That gaping artery, like the hole in someone’s neck, red from the inside and spurting out light like blood and fire. His ma had to go dig at the beast’s insides, searchin’ for metals, then escape its anger. You could only get lucky so many times.

Then he spotted it. Light. With relief, he glanced out the window and saw someone walking along the path, holding up a lantern to illuminate her way. Wayne scrambled to hide the cards under the mat, then lay on top, feigning sleep when the door opened. She’d have seen his light go out of course, but she appreciated the effort he put into pretending.

She settled on the stool, and Wayne cracked an eye. His ma wore trousers and a buttoned shirt, her hair up, her clothing and face smudged. She sat staring at the flame in the lantern, watching it flicker and dance, and her face seemed more hollow than it had been before. Like someone was taking a pickaxe to her cheeks.

That mine’s eatin’ her away, he thought. It hasn’t gobbled her up like it did Pa, but it’s gnawing on her.

Ma blinked, then fixated on something else. A card he’d left on the table. Aw, hell.

She picked it up, then looked right at him. He didn’t pretend to be asleep no more. She’d dump water on him.
“Wayne,” she said, “where did you get these cards?”
“Don’t remember.”
“Wayne . . .”
“Found ’em,” he said.

She held out her hand, and he reluctantly pulled the deck out and handed it over. She tucked the card she’d found into the box. Damn. She’d spend a day searching Tinweight for whoever had “lost” them. Well, he wouldn’t have her losing more sleep on account of him.

“Tark Vestingdow,” Wayne mumbled. “They was inna pocket of his overalls.”
“Thank you,” she said softly.
“Ma, I’ve gotta learn cards. That way I can earn a good livin’ and care for us.”
“A good livin’?” she asked. “With cards?”
“Don’t worry,” he said quickly. “I’ll cheat! Can’t make a livin’ if you don’t win, see.”

She sighed, rubbing her temples.
Wayne glanced at the cards in their stack. “Tark,” he said. “He’s Terris. Like Pa was.”
“Yes.”
“Terris people always do what they’re told. So what’s wrong with me?”
“Nothing’s wrong with you, love,” she said. “You just haven’t got a good parent to guide you.”

“Ma,” he said, scrambling off the mat to take her arm. “Don’t talk like that. You’re a great ma.”

She hugged him to her side, but he could feel her tension. “Wayne,” she asked, “did you take Demmy’s pocketknife?”

“He talked?” Wayne said. “Rust that rustin’ bastard!”
“Wayne! Don’t swear like that.”
“Rust that rusting bastard!” he said in a railworker’s accent instead.
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

# List to store audio arrays
audio_arrays = []

# Process each chunk and generate audio
for idx, chunk in enumerate(text_chunks):
    wav = tts.tts(text=chunk, speaker_wav="/home/nim/Documents/kate_1_2_much_longer.wav", language="en")
    audio_arrays.append(wav)  # Store the audio array

# Concatenate all audio arrays into one
combined_audio = np.concatenate(audio_arrays)

# Save the combined audio to a single WAV file
output_filename = 'concat_last_metal_ref_kate_1_2_much_longer.wav'
sf.write(f"//home/nim/{output_filename}", combined_audio, samplerate=22050)
print(f"Audio saved as {output_filename}")

