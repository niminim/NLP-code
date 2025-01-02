import os
import re
from pydub import AudioSegment


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