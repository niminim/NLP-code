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



########## Locate chapters

# Find all occurrences of chapters
def find_chapter_locations(text, chapters):
    results = {}

    for chapter in chapters:
        # Match chapter titles preceded and followed by newlines
        pattern = rf'(?<!\S){re.escape(chapter)}(?!\S)'  # Matches standalone words, avoiding word boundaries (is more flexible for in-line standalone matches

        matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]

        # Store the results for each chapter in a dictionary
        results[chapter] = matches

    return results


# filter out non-beginning occurrences
def filter_non_beginnings(chapter_locations):
    filtered_chapters = {}

    for chapter, locations in chapter_locations.items():
        if locations:  # Ensure there are matches
            # Keep only the first occurrence (smallest start position)
            first_occurrence = min(locations, key=lambda loc: loc[0])
            filtered_chapters[chapter] = first_occurrence

    return filtered_chapters


# Sort chapters by their starting position
def sort_chapters_by_position(chapter_locations):
    """
    Sorts a list of chapter occurrences by their starting positions.

    Args:
        chapter_locations (list): A list of tuples in the form [('Chapter Name', (start, end)), ...].

    Returns:
        list: A sorted list of tuples by the starting position.
    """
    return sorted(chapter_locations, key=lambda x: x[1][0])


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


def find_chapter_locations2(text, chapters):
    """
    Finds all occurrences of chapter titles in the text where the chapter name is the only content in the line,
    and returns results as a list of tuples in the format: [('Chapter Name', (start, end))].

    Args:
        text (str): The input text to search.
        chapters (list of str): A list of chapter titles to look for.

    Returns:
        list: A list of tuples where each tuple contains the chapter title and its (start, end) positions.
    """
    results = []

    for chapter in chapters:
        # Match chapter titles that appear as the only content on the line
        pattern = rf'^(?<!\S){re.escape(chapter)}(?!\S)$'  # Matches entire line with the chapter title

        # Find all matches with start and end positions
        matches = [(match.start(), match.end()) for match in re.finditer(pattern, text, re.MULTILINE)]

        # Add chapter name and its positions to the results
        for start, end in matches:
            results.append((chapter, (start, end)))

    return results


def get_chapter_text(chapters_dict, chapters, chapter_idx):
    # the function gets the chapters list and the chapter idx and return the corresponding text
    chapter_info = chapters_dict[chapters[chapter_idx]]
    chapter_start = chapter_info['name_start']
    chapter_end = chapter_info['chapter_end']
    chapter_text = epub_content[chapter_start:chapter_end]
    print(chapter_text)
    return chapter_text, chapter_info

########## End of Locate chapters

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
# def replace_newline_sequences(input_text):
#     # Replace 3 or more newline characters with "  An ornamental break  ."
#     return re.sub(r'\n{3,}', '  ', input_text)


def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    - Example: Replace sequences of 4+ newlines with 'New section - '.
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


def process_chunk_replace_quotes_newlines(input_text):
    """
    Replaces instances of '"' followed by one or more '\n' characters followed by '"' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    return re.sub(r'"\n{1,}"', '" "', input_text)


def replace_right_quote_newline(input_text):
    """
    Replaces instances of '”\n' with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    return re.sub(r'”\n', ' ', input_text)


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



# def process_newlines(text): # this was used and worked
#     """
#     Replaces any occurrence of '\n' (single or multiple) with a single space.
#
#     Args:
#         text (str): The input text.
#
#     Returns:
#         str: The modified text with all '\n' sequences replaced by a single space.
#     """
#     # Replace any sequence of \n (one or more) with a single space
#     return re.sub(r'\n+', ' ', text)


# def process_newlines(text):
#     """
#     Replaces sequences of multiple '\n' with ' \n ' (a space, a newline, and another space),
#     and ensures single '\n' is surrounded by exactly one space, but avoids adding redundant spaces.
#
#     Args:
#         text (str): The input text.
#
#     Returns:
#         str: The modified text with '\n' properly normalized.
#     """
#     # Replace multiple \n with ' \n '
#     text = re.sub(r'\n{2,}', ' \n ', text)
#
#     # Ensure a single \n is surrounded by a single space, avoiding duplicate spaces
#     text = re.sub(r' ?\n ?', ' \n ', text)
#
#     return text

######## End of Clean text


###### Chapter_start
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

def keep_n_sequences_with_position(input_text, n):
    """
    Keeps the first n newline sequences intact, replaces the rest with spaces,
    and returns the ending position of the nth sequence.

    Parameters:
    - input_text (str): The input text to process.
    - n (int): The number of newline sequences to retain.

    Returns:
    - tuple: (processed_text, end_position_of_nth_sequence)
    """
    # Split the input text into sequences based on newlines
    sequences = re.split(r'(\n+)', input_text)

    # Calculate the indices to retain
    retain_indices = 2 * n - 1  # Each sequence has a preceding text and newline part

    # Join retained parts
    retained_part = ''.join(sequences[:retain_indices + 1])

    # Replace the rest with spaces
    replaced_part = ''.join(sequences[retain_indices + 1:]).replace('\n', ' ')

    # Combine both parts
    processed_text = retained_part + replaced_part

    # Calculate the ending position of the nth newline sequence
    nth_sequence_text = ''.join(sequences[:retain_indices + 1])
    end_position_of_nth_sequence = len(nth_sequence_text)

    return processed_text, end_position_of_nth_sequence


def keep_n_sequences(input_text, n=2):
    processed_text, end_position_of_nth_sequence = keep_n_sequences_with_position(input_text, n=2)

    # Modify the text from the nth sequence onward
    # Here, we apply `clean_newline` to the portion after the nth sequence
    chunk_to_modify = processed_text[end_position_of_nth_sequence:]
    modified_chunk = ''.join([process_chunk_replace_quotes_newline(chunk) for chunk in chunk_to_modify])
    final_text = processed_text[:end_position_of_nth_sequence] + modified_chunk

    return final_text

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
###### End of Chapter_start


def get_ref_name(ref):
    refs = {'kate_1_2_much_longer' : 'kate',
            'amanda' : 'amanda',
            'ralph' : 'ralph'}

    return refs[ref]

######## Finalize files
def chapter_idx_str(chapter_idx, start_zero):
    """
    Returns the formatted chapter number based on the chapter index and starting point,
    with a '-' appended at the end.

    Args:
        chapter_idx (int): The chapter index (e.g., 0, 1, 2, etc.).
        start_zero (bool): If True, chapter numbers start from 0. If False, start from 1.

    Returns:
        str: The formatted chapter number as a string in the form "00-", "01-", etc.
    """
    chapter_number = chapter_idx if start_zero else chapter_idx + 1
    return f"{chapter_number:02d}-"


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

# Path to your EPUB file
file_path = '/home/nim/Downloads/The_Dragons_of_Krynn.epub'
epub_content = read_epub(file_path)


# Print a portion of the EPUB content
# print(epub_content[8000:10000])  # Print the first 1000 characters

ref = 'ralph' # kate_1_2_much_longer, amanda_leigh2, ralph, rebecca
chunk_size = 350
audio_format = 'wav'
ref_name = get_ref_name(ref) # kate, amanda, ralph
start_zero = True # True if we have a prologue (or something else), False if we start from chapter 1

base = '/home/nim'
book_name = 'The_Dragons_of_Krynn_NEW3' + f"_by_{ref_name}_{chunk_size}"
book_path = os.path.join(base, book_name)


# List of chapters to find
chapters = ['Seven Hymns of the Dragon', 'The Final Touch', 'Night of Falling Stars', 'Honor Is All', 'Easy Pickings', 'A Dragon to the Core',
            'Dragon Breath', "Fool's Gold", 'Scourge of the Wicked Kendragon', 'And Baby Makes Three',
            'The First Dragonarmy Bridging Company', 'The Middle of Nowhere', "Kaz and the Dragon's Children",
            "Into the Light", "The Best", "The Hunt"]


# Find all locations of chapter titles
chapter_locations = find_chapter_locations2(epub_content, chapters)
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)


# # Print the chapter locations
# for chapter, locations in chapter_locations.items():
#     print(f"'{chapter}' found at positions: {locations}")


device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


# for chapter_idx in [1,2,3,4,5,6,7,10,11,12,13,14]:
for chapter_idx in [8]:

    chapter_text, chapter_info = get_chapter_text(chapters_dict, chapters, chapter_idx)

    chapter_name = chapters[chapter_idx]
    chapter_name_adj = chapter_name.replace(' ', '_')
    chapter_folder =  os.path.join(book_path, chapter_name_adj)
    os.makedirs(chapter_folder, exist_ok=True)

    if chapter_idx == 0:
        chapter_text = convert_latin_numbers_to_words(chapter_text)

    chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)
    chapter_chunks[1:] = [process_chunk_add_new_section(chunk) for chunk in chapter_chunks[1:]] # Pay attention here to the num of \n (especially for paragraphs
    chapter_chunks[1:] = [process_chunk_replace_quotes_newline(chunk) for chunk in chapter_chunks[1:]] # There's also a function for newlines
    chapter_chunks[1:] = [replace_newline_after_quote(chunk) for chunk in chapter_chunks[1:]]
    chapter_chunks[1:] = [replace_right_quote_newline(chunk) for chunk in chapter_chunks[1:]]

    # Deal with the header
    chapter_chunks[0] = keep_n_sequences(chapter_chunks[0], n=2)
    # chapter_chunks[0] = add_newline_after_chapter_name(chapter_chunks[0], chapter_name)


    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter {chapter_idx+1} - Processing chunks")):
        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        if idx == 38:
            break


    # # Concat parts to assemble the chapter
    chapter_str = chapter_idx_str(chapter_idx, start_zero)
    output_file = os.path.join(book_path, chapter_str + chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)

    # Sleep for 20 seconds
    time.sleep(20)

    ### IT STILL RUNS IN NEW 3  !!!!
