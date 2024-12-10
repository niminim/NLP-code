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


def efficient_split_text_to_chunks(text, max_length):
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


def clean_text(chunk):
    chunk = chunk.replace("\\'", "'")
    chunk = chunk.replace("...", "").replace("..", "")
    return chunk

def replace_single_newline_with_blank(text):
    """
    Replaces single occurrences of '\n' with a blank space,
    leaving sequences of multiple '\n' untouched.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with single '\n' replaced by a blank space.
    """
    return re.sub(r'(?<!\n)\n(?!\n)', ' ', text) # Matches a \n that is not preceded by another \n ((?<!\n) ensures this).


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
            'amanda_leigh2' : 'amanda',
            'ralph' : 'ralph'}

    return refs[ref]

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
file_path = '/home/nim/Downloads/Baroness_of_Blood.epub'
epub_content = read_epub(file_path)


# Print a portion of the EPUB content
# print(epub_content[8000:10000])  # Print the first 1000 characters

ref = 'ralph' # kate_1_2_much_longer, amanda_leigh2, ralph, rebecca
chunk_size = 350
audio_format = 'wav'
ref_name = get_ref_name(ref) # kate, amanda, ralph

base = '/home/nim'
book_name = 'Baroness_of_Blood' + f"_by_{ref_name}_{chunk_size}"
book_path = os.path.join(base, book_name)


# List of chapters to find
chapters = ['Prologue', 'One', 'Two', 'Three', 'Four','Five', 'Six', 'Seven','Eight', 'Nine','Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
            'Fifteen','Sixteen', 'Seventeen', 'Eighteen', 'Nineteen','Twenty', 'Twenty-one', 'wenty-two', 'Twenty-three',
            'Twenty-four', 'Twenty-seven', 'Twenty-six', 'Twenty-seven','Twenty-eight', 'Twenty-nine', 'Thirty', 'Thirty-one','Epilogue']


# Find all locations of chapter titles
chapter_locations = find_chapter_locations(epub_content, chapters)
chapter_locations = filter_non_beginnings(chapter_locations)
sorted_chapters = sort_chapters_by_position(chapter_locations)
chapters_dict = create_chapters_dict(sorted_chapters, epub_content)

# # Print the chapter locations
# for chapter, locations in chapter_locations.items():
#     print(f"'{chapter}' found at positions: {locations}")


chunk1 = epub_content[0:500]
chunk2 = epub_content[500:1000]
chunk3 = epub_content[1000:1500]
chunk4 = epub_content[1500:2000]

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

filepath1 = os.path.join(book_path, "file1.wav")
filepath2 = os.path.join(book_path, "file2.wav")
filepath3 = os.path.join(book_path, "file3.wav")
filepath4 = os.path.join(book_path, "file4.wav")

tts.tts_to_file(text=chunk1, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath1)
tts.tts_to_file(text=chunk2, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath2)
tts.tts_to_file(text=chunk3, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath3)
tts.tts_to_file(text=chunk4, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath4)


for chapter_idx in [5,1,5,6]:
# for chapter_idx in [15]:
    # chapter_idx = 15 # 8, 2, 3, 0, 15, 4, 1, 5, 6, 7, 9, 10 ,11, 12, 13
    chapter_text, chapter_info = get_chapter_text(chapters, chapter_idx)



    chapter_name = chapters[chapter_idx]
    chapter_name_adj = chapter_name.replace(' ', '_')
    chapter_folder =  os.path.join(book_path, chapter_name_adj)
    os.makedirs(chapter_folder, exist_ok=True)

    if chapter_idx == 0:
        chapter_text = convert_latin_numbers_to_words(chapter_text)


    chapter_chunks = efficient_split_text_to_chunks(chapter_text, max_length=chunk_size)
    chapter_chunks = [clean_text(chunk) for chunk in chapter_chunks]
    chapter_chunks = [replace_single_newline_with_blank(chunk) for chunk in chapter_chunks]
    chapter_chunks[0] = add_newline_after_chapter_name(chapter_chunks[0], chapter_name)


    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Process each chunk and generate audio
    for idx, chunk in enumerate(tqdm(chapter_chunks, desc=f"chapter {chapter_idx+1} - Processing chunks")):
        filepath = os.path.join(chapter_folder, f"part{idx + 1}.wav")
        print(chunk)
        tts.tts_to_file(text=chunk, speaker_wav=f"/home/nim/Documents/{ref}.wav", language="en", file_path=filepath)

        # if idx == 8:
        #     break


    # Concat parts to assemble the chapter
    output_file = os.path.join(book_path, chapter_name_adj + f".{audio_format}")  # Replace with your output file path
    concat_wavs_in_folder(chapter_folder, output_file, format=audio_format)


