import os
import re
import numpy as np
import json


def get_dirs(base, book_name, ref):
    book_dir = f"{book_name}_by_{ref}_350" # The_Dragons_of_Krynn_NEW5_by_ralph_lister_350
    book_path = os.path.join(base, book_dir)
    json_dir = os.path.join(book_path, "texts", "comparisons")
    os.makedirs(json_dir, exist_ok=True)
    orig_chunks_dir = f"{book_path}/texts/orig_chunks"
    transcribed_dir = f"{book_path}/texts/transcriptions"

    return book_path, json_dir, orig_chunks_dir, transcribed_dir


def open_text_file(file_path, encoding="utf-8"):
    """
    Opens and reads a text file, handling errors gracefully.

    Args:
        file_path (str): Path to the text file.
        encoding (str): Encoding used to read the file. Default is "utf-8".

    Returns:
        str: Content of the text file if successful, None otherwise.
    """
    try:
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred while reading the file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")


def read_json_file(file_path):
    """
    Reads a JSON file and returns its content as a Python dictionary.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: The content of the JSON file as a Python dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from file '{file_path}'. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{file_path}': {e}")
    return None



def get_sorted_text_files(chapter_dir):
    """
    List and sort files in a directory by their part number.

    Args:
        chapter_dir (str): Path to the directory containing files.

    Returns:
        list: Sorted list of file names by part number.
    """

    # Check if the directory exists
    if not os.path.exists(chapter_dir):
        print(f"Error: The directory '{chapter_dir}' does not exist.")
        return []  # Return an empty list or handle as needed

    # List all files in the directory
    files = os.listdir(chapter_dir)

    # Filter files matching the 'part<number>' pattern
    part_files = [file for file in files if re.match(r'part\d+', file)]

    # Sort files by extracting the part number
    part_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    return part_files


# Text Normalization Function
def normalize_text(text):
    """
    Normalize the text by converting to lowercase, replacing all types of dashes with spaces,
    removing punctuation, and removing extra spaces.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[—–-]', ' ', text)  # Replace all types of dashes with spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove other punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# WER Calculation
def calculate_wer(original_text, transcribed_text):
    """
    Calculate the Word Error Rate (WER) between the original and transcribed texts.
    """
    original_words = original_text.split()
    transcribed_words = transcribed_text.split()

    # Create a matrix for dynamic programming
    dp = np.zeros((len(original_words) + 1, len(transcribed_words) + 1), dtype=int)
    for i in range(len(original_words) + 1):
        dp[i][0] = i
    for j in range(len(transcribed_words) + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, len(original_words) + 1):
        for j in range(1, len(transcribed_words) + 1):
            if original_words[i - 1] == transcribed_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = min(
                    dp[i - 1][j],  # Deletion
                    dp[i][j - 1],  # Insertion
                    dp[i - 1][j - 1]  # Substitution
                ) + 1

    # WER = (S + D + I) / N
    wer = dp[len(original_words)][len(transcribed_words)] / len(original_words)
    return round(wer, 3)


# CER Calculation
def calculate_cer(original_text, transcribed_text):
    """
    Calculate the Character Error Rate (CER) between the original and transcribed texts.
    """
    original_chars = list(original_text)
    transcribed_chars = list(transcribed_text)

    # Create a matrix for dynamic programming
    dp = np.zeros((len(original_chars) + 1, len(transcribed_chars) + 1), dtype=int)
    for i in range(len(original_chars) + 1):
        dp[i][0] = i
    for j in range(len(transcribed_chars) + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, len(original_chars) + 1):
        for j in range(1, len(transcribed_chars) + 1):
            if original_chars[i - 1] == transcribed_chars[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = min(
                    dp[i - 1][j],  # Deletion
                    dp[i][j - 1],  # Insertion
                    dp[i - 1][j - 1]  # Substitution
                ) + 1

    # CER = (S + D + I) / N
    cer = dp[len(original_chars)][len(transcribed_chars)] / len(original_chars)
    return round(cer, 3)


def compare_texts(original, transcribed):
    # perform the comparison between two texts - the original and the transcribed

    # Normalize the texts
    original_normalized = normalize_text(original)
    transcribed_normalized = normalize_text(transcribed)

    # Calculate WER, CER, and the length difference
    wer = calculate_wer(original_normalized, transcribed_normalized)
    cer = calculate_cer(original_normalized, transcribed_normalized)
    len_diff = len(original_normalized.split()) - len(transcribed_normalized.split())

    # Return results in a dictionary
    return {
        "original_normalized": original_normalized,
        "transcribed_normalized": transcribed_normalized,
        "WER": wer,
        "CER": cer,
        "len_diff": len_diff,
    }

def update_evaluation_data(evaluation_data, chapter, part, compare_texts_res):
    """
    Updates the evaluation data dictionary with the results for a specific part of a chapter.
    """
    # Ensure the chapter key exists in the dictionary
    if f"chapter {chapter}" not in evaluation_data:
        evaluation_data[f"chapter {chapter}"] = {}

    # Add or update the part data
    evaluation_data[f"chapter {chapter}"][f"Part {part}"] = {
        "original_text": compare_texts_res['original_normalized'],
        "transcribed_text": compare_texts_res['transcribed_normalized'],
        "original_text_len": len(compare_texts_res['original_normalized'].split()),
        "transcribed_text_len": len(compare_texts_res['transcribed_normalized'].split()),
        "len_diff" :  compare_texts_res['len_diff'],
        "WER": f"{compare_texts_res['WER']:.2%}",
        "CER": f"{compare_texts_res['CER']:.2%}"
    }


def update_parts_to_correct(to_correct, chapter, part):
    chapter_key = f"{chapter}"
    if chapter_key not in to_correct:
        to_correct[chapter_key] = []
    to_correct[chapter_key].append(part)


def find_files_with_prefix_and_format(folder_path, prefix, file_format):
    """
    Find all files in a folder that start with a specific prefix and have a specific file format.

    Args:
        folder_path (str): Path to the folder to search.
        prefix (str): Prefix that the files should start with.
        file_format (str): File extension (e.g., ".txt", ".csv") to match.

    Returns:
        list: List of full file paths that match the specified prefix and file format.
    """
    matching_files = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file starts with the prefix and ends with the specified file format
        if file_name.startswith(prefix) and file_name.endswith(file_format):
            # Add the full path to the list
            matching_files.append(os.path.join(folder_path, file_name))

    return matching_files


def get_sorted_part_numbers(folder_path):
    """
    Extract unique part numbers (e.g., '119') from filenames in the specified folder
    and order them numerically.

    Args:
        folder_path (str): Path to the folder containing the files.

    Returns:
        list: A sorted list of unique part numbers as integers.
    """
    part_numbers = set()  # Use a set to ensure uniqueness

    # Regular expression to match part names (e.g., 'part119') and extract the number
    part_pattern = re.compile(r"^part(\d+)")

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        match = part_pattern.match(file_name)  # Match the part name and extract the number
        if match:
            part_numbers.add(int(match.group(1)))  # Extract the number and convert to integer

    # Return the sorted list of part numbers
    return sorted(part_numbers)


def update_fix_chapters_stats(fix_chapters_stats, chapter, part, rep_idx, fix_compare_texts_res, orig_part_stats):
    fix_chapters_stats[chapter][part][rep_idx + 1] = {
        'original_text': orig_part_stats['original_text'],
        'transcribed_text': orig_part_stats['transcribed_text'],
        'fixed_transcribed_text': fix_compare_texts_res['transcribed_normalized'],
        "original_text_len": orig_part_stats['original_text_len'],
        "transcribed_text_len": orig_part_stats['transcribed_text_len'],
        "fix_transcribed_text_len": len(fix_compare_texts_res['transcribed_normalized'].split()),
        'WER': f"{fix_compare_texts_res['WER']:.2%}",
        'CER': f"{fix_compare_texts_res['CER']:.2%}",
        'len_diff': fix_compare_texts_res['len_diff']
    }