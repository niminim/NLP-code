import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from pydub import AudioSegment
import os

from tqdm import tqdm

import torch
from TTS.api import TTS


def read_epub(file_path):
    # Function reads the EPUB content
    book = epub.read_epub(file_path)

    # To store all the text content from the EPUB
    all_text = []

    # Iterate over the book items
    for item in book.get_items():
        # Only extract the documents that are of type XHTML
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Use BeautifulSoup to extract text from the HTML content
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            all_text.append(soup.get_text())

    return '\n'.join(all_text)



# Improved function to find all occurrences of chapters
def find_chapter_locations(text, chapters):
    results = {}

    for chapter in chapters:
        # Match chapter titles preceded and followed by newlines
        pattern = rf'(?<!\S){re.escape(chapter)}(?!\S)'  # Matches standalone words, avoiding word boundaries (is more flexible for in-line standalone matches

        matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]

        # Store the results for each chapter in a dictionary
        results[chapter] = matches

    return results

# Function to filter out non-beginning occurrences
def filter_non_beginnings(chapter_locations):
    filtered_chapters = {}

    for chapter, locations in chapter_locations.items():
        if locations:  # Ensure there are matches
            # Keep only the first occurrence (smallest start position)
            first_occurrence = min(locations, key=lambda loc: loc[0])
            filtered_chapters[chapter] = first_occurrence

    return filtered_chapters

# Function to sort chapters by their starting position
def sort_chapters_by_position(chapter_locations):
    # Convert dictionary to a list of tuples and sort by the starting position (first element of the tuple)
    sorted_chapters = sorted(chapter_locations.items(), key=lambda x: x[1][0])
    return sorted_chapters


def create_chapters_dict(sorted_chapters, epub_content):
    # the function creates a dictionary with starts and beginings of each chapter
    chapters_dict = {}
    for i, chapter_data in enumerate(sorted_chapters):
        if i < len(sorted_chapters) - 1:

            chapters_dict[chapter_data[0]] = {'name': epub_content[chapter_data[1][0]: chapter_data[1][1]],
                                              'name_start': chapter_data[1][0],
                                              'name_end': chapter_data[1][1],
                                              'chapter_end': sorted_chapters[i + 1][1][0] - 1,
                                              'length': sorted_chapters[i + 1][1][0] - 1 - chapter_data[1][0]
                                              }
        else:
            chapters_dict[chapter_data[0]] = {'name': epub_content[chapter_data[1][0]: chapter_data[1][1]],
                                              'name_start': chapter_data[1][0],
                                              'name_end': chapter_data[1][1],
                                              'chapter_end': len(epub_content),
                                              'length':  len(epub_content) - chapter_data[1][0]
                                              }

    return chapters_dict

def get_chapter_text(chapters, chapter_idx):
    chapter_info = chapters_dict[chapters[chapter_idx]]
    chapter_start = chapter_info['name_start']
    chapter_end = chapter_info['chapter_end']
    chapter_text = epub_content[chapter_start:chapter_end]
    print(chapter_text)
    return chapter_text, chapter_info


def split_text_to_chunks(text, max_length):
    """
    Splits text into chunks based on the assigned maximum length, prioritizing:
    1. Sequences of 3 or more newlines (\n\n\n).
    2. The largest part that ends with a '.' (capped by max_length).
    3. The largest part ending with whitespace (capped by max_length).

    Args:
        text (str): The input text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0
    newline_pattern = re.compile(r'\n{3,}')  # Match sequences of 3+ newlines

    while start < len(text):
        end = min(start + max_length, len(text))

        # Find the first match of 3+ newlines in the range
        newline_match = newline_pattern.search(text, start, end)

        if newline_match:
            # Split at the newline sequence
            boundary = newline_match.start()
        else:
            # Find the largest part that ends with '.'
            last_period = text.rfind('.', start, end)
            if last_period != -1:
                boundary = last_period + 1  # Include the period
            else:
                # Fallback to the largest part ending with whitespace
                last_whitespace = text.rfind(' ', start, end)
                boundary = last_whitespace if last_whitespace != -1 else end

        # Add the chunk
        chunks.append(text[start:boundary].strip())
        start = boundary  # Update start for the next chunk

    return chunks


def clean_text(chunk):
    chunk = chunk.replace("\\'", "'")
    chunk = chunk.replace("...", "").replace("..", "")
    return chunk


def split_text_to_chunks(text, max_length):
    """
    Splits text into the largest possible chunks based on the assigned maximum length,
    ensuring each chunk ends at the shortest valid boundary:
    - A sentence boundary ('.')
    - A sequence of 3 or more newlines (e.g., \n\n\n).
    If neither is found, splits at the nearest whitespace.

    Args:
        text (str): The input text to split.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    chunks = []
    start = 0
    # Match '.' or sequences of 3+ \n
    pattern = re.compile(r'\.|(?<=\n)\n{2,}')

    while start < len(text):
        # Determine the maximum range for the current chunk
        end = min(start + max_length, len(text))

        # Find all matches for boundaries within the range
        matches = list(pattern.finditer(text, start, end))

        if matches:
            # Find the closest valid boundary within the range
            boundary = min(match.end() - 1 for match in matches if match.end() - 1 <= end)
        else:
            # Fallback: Find the last whitespace within the range
            boundary = text.rfind(' ', start, end)
            if boundary == -1:  # If no whitespace is found, split at max length
                boundary = end

        # Add the chunk
        chunks.append(text[start:boundary].strip())
        start = boundary + 1  # Move to the next position after the boundary

    return [chunk for chunk in chunks if chunk]  # Remove empty chunks

def add_newline_after_chapter_name(text, chapter_name):
    """
    Adds a newline after the chapter name if it appears at the beginning of the text.

    Args:
        text (str): The input text.
        chapter_name (str): The chapter name to check and replace (default is "Scourge of the Wicked Kendragon").

    Returns:
        str: The modified text with a newline added after the chapter name.
    """
    if text.startswith(chapter_name):
        return text.replace(chapter_name, chapter_name + '\n', 1)
    return text

def get_ref_name(ref):
    refs = {'kate_1_2_much_longer' : 'kate',
            'amanda' : 'amanda',
            'ralph' : 'ralph'}

    return refs[ref]

def replace_seven_or_more_newlines(text):
    """
    Replaces sequences of seven or more newline characters (\n\n\n\n\n\n\n or more)
    with " \n Pause here \n ".

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with sequences of 7+ newlines replaced.
    """
    # Replace sequences of 7 or more \n with " \n Pause here \n "
    text = re.sub(r'\n{7,}', ' Pause here ', text)
    return text

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


def convert_latin_numbers_to_words(text):
    """
    Converts Latin numerals (I. to X.) into their word equivalents followed by '-'.
    Does nothing for Latin numerals without a '.'.

    Args:
        text (str): Input text containing Latin numerals.

    Returns:
        str: Text with Latin numerals followed by '.' replaced by words followed by '-'.
    """
    # Mapping of Latin numerals (with '.') to their word equivalents
    latin_to_words = {
        '\nI.': ' One -', '\nII.': ' Two -', '\nIII.': ' Three -', '\nIV.': ' Four -',
        '\nV.': ' Five -', '\nVI.': ' Six -', '\nVII.': ' Seven -', '\nVIII.': ' Eight -',
        '\nIX.': ' Nine -', '\nX.': ' Ten -'
    }

    # Replace numerals followed by '.' with their word equivalents
    for numeral, word in latin_to_words.items():
        text = text.replace(numeral, word)

    return text

#############################################################################


# Path to your EPUB file
file_path = '/home/nim/Downloads/The_Dragons_of_Krynn.epub'
epub_content = read_epub(file_path)


# Print a portion of the EPUB content
# print(epub_content[8000:10000])  # Print the first 1000 characters

ref = 'ralph' # kate_1_2_much_longer, amanda_leigh2, ralph, rebecca
chunk_size = 350
audio_format = 'wav'
ref_name = get_ref_name(ref) # kate, amanda, ralph

base = '/home/nim'
book_name = 'The_Dragons_of_Krynn_NEW2' + f"_by_{ref_name}_{chunk_size}"
book_path = os.path.join(base, book_name)


# List of chapters to find
chapters = ['Seven Hymns of the Dragon', 'The Final Touch', 'Night of Falling Stars', 'Honor Is All', 'Easy Pickings', 'A Dragon to the Core',
            'Dragon Breath', "Fool's Gold", 'Scourge of the Wicked Kendragon', 'And Baby Makes Three',
            'The First Dragonarmy Bridging Company', 'The Middle of Nowhere', "Kaz and the Dragon's Children",
            "Into the Light", "The Best", "The Hunt"]


# Find all locations of chapter titles
chapter_locations = find_chapter_locations(epub_content, chapters)
chapter_locations = filter_non_beginnings(chapter_locations)
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)

# # Print the chapter locations
# for chapter, locations in chapter_locations.items():
#     print(f"'{chapter}' found at positions: {locations}")


# for chapter_idx in [1,2,3,4,5,6,7,10,11,12,13,14]:
# for chapter_idx in [1,2,5,6,7]:
for chapter_idx in [8]:

    chapter_text, chapter_info = get_chapter_text(chapters, chapter_idx)

    chapter_name = chapters[chapter_idx]
    chapter_name_adj = chapter_name.replace(' ', '_')
    chapter_folder =  os.path.join(book_path, chapter_name_adj)
    os.makedirs(chapter_folder, exist_ok=True)

    if chapter_idx == 0:
        chapter_text = convert_latin_numbers_to_words(chapter_text)

    chapter_chunks = split_text_to_chunks(chapter_text, max_length=chunk_size)
    chapter_chunks = [clean_text(chunk) for chunk in chapter_chunks]
    # chapter_chunks = [split_text_to_chunks(chunk) for chunk in chapter_chunks] # we need the first
    # chapter_chunks[0] = add_newline_after_chapter_name(chapter_chunks[0], chapter_name)


    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter {chapter_idx+1} - Processing chunks")):
        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        if idx == 40:
            break

    # # Concat parts to assemble the chapter
    output_file = os.path.join(book_path, chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)








