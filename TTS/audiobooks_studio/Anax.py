import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from pydub import AudioSegment
import os
import time

from tqdm import tqdm

import torch
from TTS.api import TTS



def efficient_split_text_to_chunks(text, max_length): # this was used and worked
    """
    Splits the text into the largest possible chunks based on the assigned maximum length,
    ensuring each chunk ends at a sentence boundary ('.') when possible.
    If no '.' is found, splits at the nearest whitespace to avoid breaking words.

    Args:
        text (str): The input text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        # Determine the furthest point for the current chunk
        end = min(start + max_length, len(text))

        # Look for the last '.' within the allowable range
        last_dot_index = text.rfind(".", start, end)

        if last_dot_index == -1:  # If no '.' is found in the range
            # Look for the last whitespace within the range
            last_space_index = text.rfind(" ", start, end)
            if last_space_index != -1:  # If a space is found, split at the space
                last_dot_index = last_space_index
            else:  # If no space is found, split at the max length
                last_dot_index = end

        # Add the chunk
        chunks.append(text[start:last_dot_index].strip())
        # Update the start to the new position
        start = last_dot_index + 1

    return [chunk for chunk in chunks if chunk]  # Remove any empty chunks


######## Clean text
def replace_newline_sequences(input_text):
    # Replace 3 or more newline characters with "  An ornamental break  ."
    return re.sub(r'\n{3,}', '  ', input_text)


def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    - Example: Replace sequences of 5+ newlines with 'New section - '.
    """
    return re.sub(r'\n{4,}', ' New section - ', chunk)


def process_chunk_replace_quotes_newline(input_text):
    """
    Replaces instances of '"' followed by '\n' followed by '"' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    return re.sub(r'"\n"', '" "', input_text)

def replace_right_quote_newline(input_text):
    """
    Replaces instances of '”\n' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    return re.sub(r'”\n', ' ', input_text)


def process_chunk_replace_quotes_newlines(input_text):
    """
    Replaces instances of '"' followed by one or more '\n' characters followed by '"' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    return re.sub(r'"\n{1,}"', '" "', input_text)


def replace_newline_after_quote(input_text):
    """
    Replaces instances of '"\n' followed by a capital letter with '" '
    and retains the capital letter.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    return re.sub(r'"\n([A-Z])', r'" \1', input_text)


######## End of Clean text


def concat_wavs_in_folder(folder_path, output_file, format='wav'):
    """
    Concatenates all WAV files in a folder in numerical order based on the part number
    in their filenames and saves them into a single WAV file.

    Args:
        folder_path (str): Path to the folder containing WAV files.
        output_file (str): Path to save the combined WAV file.

    Returns:
        None
    """
    # Function to extract the numeric part from the filename
    def extract_number(file_name):
        match = re.search(r'part(\d+)', file_name, re.IGNORECASE)
        return int(match.group(1)) if match else float('inf')  # Place non-matching files at the end

    # List all WAV files in the folder
    wav_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".wav")]

    # Sort files numerically based on the extracted number
    sorted_files = sorted(wav_files, key=extract_number)

    # Initialize an empty AudioSegment for concatenation
    combined = AudioSegment.empty()

    # Concatenate the sorted audio files
    for file_name in sorted_files:
        file_path = os.path.join(folder_path, file_name)
        print(f"Adding {file_name} to the combined audio.")
        audio = AudioSegment.from_wav(file_path)
        combined += audio

    # Export the combined audio to the specified output file
    if format.lower() == 'wav':
        combined.export(output_file, format="wav")
    elif format.lower() == 'mp3':
        combined.export(output_file, format="mp3", bitrate="320")
    print(f"All WAV files concatenated and saved as '{output_file}'.")
######## End of Finalize files


#############################################################################

text = """
"Ladies and gentlemen, we're being held up at a red signal. We should be on the move shortly."

The train conductor's announcement proves to be useless as this is the fifth time Naya has heard the words since she boarded the train more than half an hour ago. She huffs out her frustration with everyone else in the carriage before turning her attention back to the book she was reading. Just as the train pushes forward, her focus on the words lapses as her mind wanders off. She tries to wrestle it again into the written word, and she would have succeeded if it was not for the odd tingling sensation that can only mean someone's eyes are upon her.

Naya likes to think that there are a few unwritten rules when it comes to being on public transport—one of which is not staring. She can handle it most of the time, giving people that do it the benefit of the doubt that they are not aware or are simply tourists, but the intensity of this particular stare makes her apprehensive.

At half past five on a Friday afternoon, the carriage is pretty full, but Naya can still pick up on the person staring at her with no trouble. She supposes anyone could, what with how conspicuous he is—standing next to the middle set of doors, looking anything but familiar. It strikes her as odd. Usually, people turn their gaze elsewhere when they realise they have been caught, but he holds her gaze as she examines him.

He's likely taller than her, although it’s hard to determine from where she’s seated. With his dark hair and firm posture, there's nothing particularly noteworthy about him that stands out. However, Naya has a lingering feeling that she would have recognised him if they had met before. What catches her interest is that his attention appears to be more directed towards Naya than on his companion, who engages in conversation.

The train slows down once more by what must be a red signal, and just before stopping completely, it hauls forward to regain momentum to rush past again. Naya would admit to being petty enough to gloat silently as the staring man almost loses his balance, but, at the very least, it causes him to avert his glance.

Happily, Naya thinks that at least Karma still works as she tries to return to her book.

It proves futile as the robotic voice of London's underground trains announces loudly, “The next stop is Finchley Road,” so Naya tucks the book into her bag.

Something is bugging her, and she looks to her right, catching the stranger's attention again as she stands and moves to the doors. To try and relax her anxious mind, she counts the seconds until she sees the blissful sign of the station at which she needs to alight, which hopefully means good riddance to creepy passengers on the train.

Naya can't help wondering what makes him stare at her as she knows that, before leaving work, she touched up her makeup, ensuring her naturally tanned complexion is presentable. Her brown hair is somewhat loose in a bun, but it adds a touch of carefree and tousled charm to her overall look. She decides to cut herself some slack as she's just finished her tedious shift in a restaurant, and while she didn't have time to change before leaving work as she was running late, she was promised that even her waitress attire—a white button-down blouse and fitted jeans—are a good option for the evening she’s planned with her friends.

There must be something, she thinks anxiously.

As the train advances to Finchley Road’s station, Naya is hit with an unwelcome sense of alarm when she notices the two strangers getting ready to leave the train. Once the doors have opened, Naya steps out, hearing the same robotic voice, asking everyone repeatedly to mind the gap. The platform is busy as it always is during rush hour, and she squeezes past other passengers to the next platform, where she will wait for another train to take her to West Hampstead station. The men flit in and out of her focus, and she tries not to appear visibly shaken when they board the same train that she does.

There are only a few passengers on the short five-minute ride. This doesn't help her nerves, but she has the experience of knowing the station's layout, so when they arrive, she is ready to navigate the area to avoid them and hopefully shake off these remaining ominous feelings.

There’s a queue on the way out of the station, but at least she can’t see them anymore, which relaxes her.

The late October breeze helps to keep her sober-minded to the point where she can scold herself for thinking anyone is after her, and she scoffs, sliding her card by the station’s barriers and then taking a sharp right. When she does make it outside, she forces her mind to focus on more important things.

She is almost an hour late. Besides being caught up at work, she needs a reasonably good excuse to try on her friends. That statement is far too overused, and she is such a bad liar that it has never done the trick anyway, but she will do what she can to minimise the damage. The brisk walk keeps her warm, which is the only perk of being late. Before long, she is standing in front of the pub right across her flat building, hurrying to get indoors.

The pub, which is her and her friends’ usual go-to spot, hums with chatter and laughter. The scattered tables perfectly blend in as they’re made from the same dark wood as the walls and the floors, and the dim lighting creates a cosy ambience that adds additional charm. Normally, Naya would go straight to the bar, but it’s too crowded right now to even think about getting a drink.

It doesn’t take her long to spot her friends sitting at a table. She’ll never admit it out loud, but perhaps this is the other upside of being late—it takes the weight off her shoulders of needing to find a place for them to sit. It is a task and usually involves them hovering over a table until the current occupants leave. She’s glad they are sitting at one of their preferred tables—the one by the wall-length windows that overlook the back garden, which is temporarily closed due to renovations combined with the upcoming winter.

Naya takes in her friends as she makes her way to them. She gets a dirty look from one of the twins, just as she suspected she would. With their sandy hair, dark eyes, and pale complexion, they are similar enough to be confused by others. Yet, Naya had the unfair advantage of growing up with them; thus, unlike most people, she knows to relate to them as two different people. The other twin, as usual, is more sympathetic and smiles at her as he waves her way. He shares a playful look with the blonde woman sitting next to him, and they both wait to see his brother's reaction when she arrives at the table.

“Ah, her Royal Highness Naya,” he says, and Naya chuckles as an act of defiance and sits down, but not before winking at the pair next to him.
"""

text2 = """
"I think Lucas might be afraid someone will steal his throne,” Naya tells them and nudges the twin in question, earning yet another angry glance in her direction, which doesn’t cause her to back down. “I figured you’d have made sure he was onto his next drink by now so at least he’d be tolerable.”

Lucas scoffs, his eyes rolling condescendingly. “At least my go-to reaction in problem-solving isn’t drinking two bottles of wine from the fridge.”

As if to emphasize his jab, the woman casually pushes a glass filled with Naya’s all-time favorite wine, Pinot Grigio. It makes Naya smile, and she turns her attention to participate in the banter.

“No, you just sleep around,” the words roll off her tongue, and it’s oddly comforting how he laughs.

The blond woman takes a sip of her gin and tonic before saying, “Either way doesn’t sound too healthy, you know?” Her question is innocent, yet with a hint of curiosity there.

“Julie, just because you’ve had your chance—”

Julie laughs loudly, successfully shutting Lucas up. “Oh, my God! Don’t finish the sentence, please!”

Naya briefly looks over at how Lucas’s twin, Logan, falls silent, his smile disappearing. She offers him a slight glance—one she hopes is supportive and helpful—before trying to avert the subject. “Well, with all due respect to who you’re letting in your bed and who you’re not, I think we’re here for a special occasion.”

Logan grins gratefully at her and nods. He raises his beer, prompting the others to do the same, and when they do, he toasts, “To Julie!”

As they all repeat the toast, Julie sits there, completely content, watching Logan pull a colorful plastic bag that screams Happy Birthday! But before Julie can try to take it from him, Naya stops her, elbowing Lucas, who springs into action.

“Wait!” he exclaims. “The cake!”

Without waiting, he makes his way to the bar, whispering a few words to the bartender, and returns with a victorious smile as if he hadn’t just missed his cue to have Julie’s birthday cake presented at the same time as their toast.

“Unbelievable,” Naya shakes her head, though it doesn’t surprise them. “Please tell me you asked them to light the candles.”

“Hey, give me some credit.”

He doesn’t bother turning to Naya to see her raised eyebrows but waits patiently for the cake to be delivered to their table. They know this is one of the few pubs in London where they can get away with lighting birthday candles indoors, so they wait in anticipation. The cake is presented by one of the bartenders—Lucas’s friend—who leaves shortly after, ensuring they all have what they need.

Lucas begins the toast he meant to open with before. “I just want to say—”

Naya and Logan groan in annoyance, but Julie smiles, urging Lucas to go on.

He does, blatantly ignoring the other two. “Julie, thank God you met Naya. I don’t think we would have tolerated her ranting as well as you do. So, here’s to you for saving me from a heap of trouble!”

Naya rolls her eyes as Julie and Logan laugh, with Lucas soon joining them as he half hugs Naya, assuring her it was a joke. Without admitting he is right, she goes on to wish her best friend all the best.

Almost everyone in the pub joins in when Lucas starts singing Happy Birthday, and Naya takes out her phone, quick to snap a few pictures and videos of a highly cheerful Julie and then takes some of them together.

"enjoying how normal it all feels, and despite the cliché, she hopes it can stay like this forever."
"""


text_full = """
"Ladies and gentlemen, we're being held up at a red signal. We should be on the move shortly."

The train conductor's announcement proves to be useless as this is the fifth time Naya has heard the words since she boarded the train more than half an hour ago. She huffs out her frustration with everyone else in the carriage before turning her attention back to the book she was reading. Just as the train pushes forward, her focus on the words lapses as her mind wanders off. She tries to wrestle it again into the written word, and she would have succeeded if it was not for the odd tingling sensation that can only mean someone's eyes are upon her.

Naya likes to think that there are a few unwritten rules when it comes to being on public transport—one of which is not staring. She can handle it most of the time, giving people that do it the benefit of the doubt that they are not aware or are simply tourists, but the intensity of this particular stare makes her apprehensive.

At half past five on a Friday afternoon, the carriage is pretty full, but Naya can still pick up on the person staring at her with no trouble. She supposes anyone could, what with how conspicuous he is—standing next to the middle set of doors, looking anything but familiar. It strikes her as odd. Usually, people turn their gaze elsewhere when they realise they have been caught, but he holds her gaze as she examines him.

He's likely taller than her, although it’s hard to determine from where she’s seated. With his dark hair and firm posture, there's nothing particularly noteworthy about him that stands out. However, Naya has a lingering feeling that she would have recognised him if they had met before. What catches her interest is that his attention appears to be more directed towards Naya than on his companion, who engages in conversation.

The train slows down once more by what must be a red signal, and just before stopping completely, it hauls forward to regain momentum to rush past again. Naya would admit to being petty enough to gloat silently as the staring man almost loses his balance, but, at the very least, it causes him to avert his glance.

Happily, Naya thinks that at least Karma still works as she tries to return to her book.

It proves futile as the robotic voice of London's underground trains announces loudly, “The next stop is Finchley Road,” so Naya tucks the book into her bag.

Something is bugging her, and she looks to her right, catching the stranger's attention again as she stands and moves to the doors. To try and relax her anxious mind, she counts the seconds until she sees the blissful sign of the station at which she needs to alight, which hopefully means good riddance to creepy passengers on the train.

Naya can't help wondering what makes him stare at her as she knows that, before leaving work, she touched up her makeup, ensuring her naturally tanned complexion is presentable. Her brown hair is somewhat loose in a bun, but it adds a touch of carefree and tousled charm to her overall look. She decides to cut herself some slack as she's just finished her tedious shift in a restaurant, and while she didn't have time to change before leaving work as she was running late, she was promised that even her waitress attire—a white button-down blouse and fitted jeans—are a good option for the evening she’s planned with her friends.

There must be something, she thinks anxiously.

As the train advances to Finchley Road’s station, Naya is hit with an unwelcome sense of alarm when she notices the two strangers getting ready to leave the train. Once the doors have opened, Naya steps out, hearing the same robotic voice, asking everyone repeatedly to mind the gap. The platform is busy as it always is during rush hour, and she squeezes past other passengers to the next platform, where she will wait for another train to take her to West Hampstead station. The men flit in and out of her focus, and she tries not to appear visibly shaken when they board the same train that she does.

There are only a few passengers on the short five-minute ride. This doesn't help her nerves, but she has the experience of knowing the station's layout, so when they arrive, she is ready to navigate the area to avoid them and hopefully shake off these remaining ominous feelings.

There’s a queue on the way out of the station, but at least she can’t see them anymore, which relaxes her.

The late October breeze helps to keep her sober-minded to the point where she can scold herself for thinking anyone is after her, and she scoffs, sliding her card by the station’s barriers and then taking a sharp right. When she does make it outside, she forces her mind to focus on more important things.

She is almost an hour late. Besides being caught up at work, she needs a reasonably good excuse to try on her friends. That statement is far too overused, and she is such a bad liar that it has never done the trick anyway, but she will do what she can to minimise the damage. The brisk walk keeps her warm, which is the only perk of being late. Before long, she is standing in front of the pub right across her flat building, hurrying to get indoors.

The pub, which is her and her friends’ usual go-to spot, hums with chatter and laughter. The scattered tables perfectly blend in as they’re made from the same dark wood as the walls and the floors, and the dim lighting creates a cosy ambience that adds additional charm. Normally, Naya would go straight to the bar, but it’s too crowded right now to even think about getting a drink.

It doesn’t take her long to spot her friends sitting at a table. She’ll never admit it out loud, but perhaps this is the other upside of being late—it takes the weight off her shoulders of needing to find a place for them to sit. It is a task and usually involves them hovering over a table until the current occupants leave. She’s glad they are sitting at one of their preferred tables—the one by the wall-length windows that overlook the back garden, which is temporarily closed due to renovations combined with the upcoming winter.

Naya takes in her friends as she makes her way to them. She gets a dirty look from one of the twins, just as she suspected she would. With their sandy hair, dark eyes, and pale complexion, they are similar enough to be confused by others. Yet, Naya had the unfair advantage of growing up with them; thus, unlike most people, she knows to relate to them as two different people. The other twin, as usual, is more sympathetic and smiles at her as he waves her way. He shares a playful look with the blonde woman sitting next to him, and they both wait to see his brother's reaction when she arrives at the table.

“Ah, her Royal Highness Naya,” he says, and Naya chuckles as an act of defiance and sits down, but not before winking at the pair next to him.

"I think Lucas might be afraid someone will steal his throne,” Naya tells them and nudges the twin in question, earning yet another angry glance in her direction, which doesn’t cause her to back down. “I figured you’d have made sure he was onto his next drink by now so at least he’d be tolerable.”

Lucas scoffs, his eyes rolling condescendingly. “At least my go-to reaction in problem-solving isn’t drinking two bottles of wine from the fridge.”

As if to emphasize his jab, the woman casually pushes a glass filled with Naya’s all-time favorite wine, Pinot Grigio. It makes Naya smile, and she turns her attention to participate in the banter.

“No, you just sleep around,” the words roll off her tongue, and it’s oddly comforting how he laughs.

The blond woman takes a sip of her gin and tonic before saying, “Either way doesn’t sound too healthy, you know?” Her question is innocent, yet with a hint of curiosity there.

“Julie, just because you’ve had your chance—”

Julie laughs loudly, successfully shutting Lucas up. “Oh, my God! Don’t finish the sentence, please!”

Naya briefly looks over at how Lucas’s twin, Logan, falls silent, his smile disappearing. She offers him a slight glance—one she hopes is supportive and helpful—before trying to avert the subject. “Well, with all due respect to who you’re letting in your bed and who you’re not, I think we’re here for a special occasion.”

Logan grins gratefully at her and nods. He raises his beer, prompting the others to do the same, and when they do, he toasts, “To Julie!”

As they all repeat the toast, Julie sits there, completely content, watching Logan pull a colorful plastic bag that screams Happy Birthday! But before Julie can try to take it from him, Naya stops her, elbowing Lucas, who springs into action.

“Wait!” he exclaims. “The cake!”

Without waiting, he makes his way to the bar, whispering a few words to the bartender, and returns with a victorious smile as if he hadn’t just missed his cue to have Julie’s birthday cake presented at the same time as their toast.

“Unbelievable,” Naya shakes her head, though it doesn’t surprise them. “Please tell me you asked them to light the candles.”

“Hey, give me some credit.”

He doesn’t bother turning to Naya to see her raised eyebrows but waits patiently for the cake to be delivered to their table. They know this is one of the few pubs in London where they can get away with lighting birthday candles indoors, so they wait in anticipation. The cake is presented by one of the bartenders—Lucas’s friend—who leaves shortly after, ensuring they all have what they need.

Lucas begins the toast he meant to open with before. “I just want to say—”

Naya and Logan groan in annoyance, but Julie smiles, urging Lucas to go on.

He does, blatantly ignoring the other two. “Julie, thank God you met Naya. I don’t think we would have tolerated her ranting as well as you do. So, here’s to you for saving me from a heap of trouble!”

Naya rolls her eyes as Julie and Logan laugh, with Lucas soon joining them as he half hugs Naya, assuring her it was a joke. Without admitting he is right, she goes on to wish her best friend all the best.

Almost everyone in the pub joins in when Lucas starts singing Happy Birthday, and Naya takes out her phone, quick to snap a few pictures and videos of a highly cheerful Julie and then takes some of them together.

"enjoying how normal it all feels, and despite the cliché, she hopes it can stay like this forever."
"""


ref = 'ella_lynch2' # kate_reading, amanda_leigh, ralph, rebecca,
# helen_keeley, jenna_coleman, ella_lynch, ella_lynch2, billie_brown, kim_bretton, imogen_church, cathleen_mccarron, jessica_ball, perdita_weeks,
# eleanor_tomlinson, olivia_vinall, fiona_hardingham, gemma_whelan, tuppence_middleton, daisy_edgar_jones, emilia_clarke
# pippa_bennett_warner, rosie_jones, lydia_wilson

chunk_size = 350
audio_format = 'wav'

base = '/home/nim'

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

name = "Anax"
chapter_folder = os.path.join(base, name)
os.makedirs(chapter_folder, exist_ok=True)


chapter_chunks = efficient_split_text_to_chunks(text_full, max_length=chunk_size)
chapter_chunks = [process_chunk_add_new_section(chunk) for chunk in chapter_chunks] # Pay attention here to the num of \n (especially for paragraphs
chapter_chunks = [process_chunk_replace_quotes_newline(chunk) for chunk in chapter_chunks] # There's also a function for newlines
chapter_chunks = [replace_newline_after_quote(chunk) for chunk in chapter_chunks]
chapter_chunks = [replace_right_quote_newline(chunk) for chunk in chapter_chunks]


# Process each chunk and generate audio
for idx, chunk in enumerate(tqdm(chapter_chunks)):
    filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
    print(chunk)
    tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)


# Concat parts to assemble the chapter
# # Concat parts to assemble the chapter
output_file = chapter_folder  + '/'+ f"Sample_{ref}.{audio_format}"  # Replace with your output file path
concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)



