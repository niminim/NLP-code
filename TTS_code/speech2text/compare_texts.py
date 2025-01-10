import os
import re
import numpy as np
import json


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
    except PermissionError:
        print(f"Error: Permission denied to read the file '{file_path}'.")
    except IOError as e:
        print(f"Error: An I/O error occurred while reading the file '{file_path}': {e}")
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
    Normalize the text by converting to lowercase, removing punctuation, and extra spaces.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
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


def update_evaluation_data(evaluation_data, chapter, part, original, transcribed, wer, cer):
    """
    Updates the evaluation data dictionary with the results for a specific part of a chapter.
    """
    # Ensure the chapter key exists in the dictionary
    if f"chapter {chapter}" not in evaluation_data:
        evaluation_data[f"chapter {chapter}"] = {}

    # Add or update the part data
    evaluation_data[f"chapter {chapter}"][f"Part {part}"] = {
        "original_text": original,
        "transcribed_text": transcribed,
        "original_text_len": len(original.split()),
        "transcribed_text_len": len(transcribed.split()),
        "WER": f"{wer:.2%}",
        "CER": f"{cer:.2%}"
    }

# Example Usage
if __name__ == "__main__":

    base = "/home/nim"
    book = "Baroness_of_Blood2_by_ralph_lister_350" # Baroness_of_Blood2_by_ralph_lister_350, King_of_the_Dead_by_scott_brick_350
    # The_Dragons_of_Krynn_NEW5_by_ralph_lister_350
    chapter = 'One' # Prologue, One
    # chapter = 'Scourge_of_the_Wicked_Kendragon'
    chapter = 'One' #

    part = '32'

    book_path = os.path.join(base, book)
    orig_text_files = get_sorted_text_files(os.path.join(book_path, "texts", "orig_chunks", chapter))


    # Initialize the data structure
    evaluation_data = {}

    for part in np.arange(1,len(orig_text_files)+1):
        print('part: ', part)
        original = open_text_file(f"{book_path}/texts/orig_chunks/{chapter}/part{part}.txt")
        transcribed = open_text_file(f"{book_path}/texts/transcriptions/{chapter}/part{part}.txt")

        # Normalize the texts
        original_normalized = normalize_text(original)
        transcribed_normalized = normalize_text(transcribed)

        # Calculate WER and CER
        wer = calculate_wer(original_normalized, transcribed_normalized)
        cer = calculate_cer(original_normalized, transcribed_normalized)

        print(f"WER: {wer:.2%}")
        print(f"CER: {cer:.2%}")
        update_evaluation_data(evaluation_data, chapter, part, original_normalized, transcribed_normalized, wer, cer)
        print('*******')

        output_folder = '/home/nim'
        filepath = os.path.join(output_folder, "uri.json")

        # Save with or without indent
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(evaluation_data, file,
                      indent=4)  # Use `indent=4` for pretty formatting or remove it for compact JSON

        print(f"JSON file saved at: {filepath}")


