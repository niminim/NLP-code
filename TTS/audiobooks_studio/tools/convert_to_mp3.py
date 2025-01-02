import os
from pydub import AudioSegment


def convert_wav_to_mp3(wav_file, output_file, bitrate="320k"):
    """
    Converts a WAV file to a high-quality MP3 file.

    Args:
        wav_file (str): Path to the input WAV file.
        output_file (str): Path to save the output MP3 file.
        bitrate (str): Bitrate for the MP3 file (default: "320k").

    Returns:
        None
    """
    try:
        # Load the WAV file
        audio = AudioSegment.from_wav(wav_file)

        # Export as MP3 with high quality
        audio.export(output_file, format="mp3", bitrate=bitrate)
        print(f"Converted '{wav_file}' to '{output_file}' with bitrate {bitrate}.")
    except Exception as e:
        print(f"Error converting '{wav_file}' to MP3: {e}")


# wav_file= '/home/nim/The_Dragons_of_Krynn_NEW_by_ralph_350/09-Scourge_of_the_Wicked_Kendragon.wav' # Path to your WAV file
# output_file= '/home/nim/The_Dragons_of_Krynn_NEW_by_ralph_350/09-Scourge_of_the_Wicked_Kendragon.mp3'  # Desired output MP3 file name
# convert_wav_to_mp3(wav_file, output_file)

base_folder = '/home/nim/Baroness_of_Blood_by_ralph_350' # the base book folder
dest_folder = os.path.join(base_folder, 'MP3') # where we'd like to put the mp3 files
os.makedirs(dest_folder, exist_ok=True)

files = os.listdir(base_folder)
# Filter files that start with a number and end with .wav
numbered_wav_files = [file for file in files if file[0].isdigit() and file.endswith('.wav')]

print(numbered_wav_files)

for filename in numbered_wav_files:
    wav_file = os.path.join(base_folder, filename)
    dest_path = os.path.join(dest_folder, filename.replace('.wav','.mp3'))
    convert_wav_to_mp3(wav_file, dest_path)


