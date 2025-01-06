import re
import torch
from TTS.api import TTS

# device = "cuda" if torch.cuda.is_available() else "cpu"
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
#
#
# c0 =  'Scourge of the Wicked Kendragon\nJanet Pack\n\n\n\n\n\n\n"But I was only… aaahhhh!"\nPropelled by the shopkeeper\'s arm, the kender Mapshaker Wanderfuss became a bird, sailing through the door and thudding into the middle of Daltigoth\'s main street. Dust clouded around the kender. Indignant and coughing, he levered himself to a sitting position'
# c5 = '" Mapshaker wandered into the forge area and continued his explanation. "I only tasted it. After all, one corner was hanging over the edge of the table."\n"I\'m busy. Go away," the smith said roughly, pumping the bellows until the roaring fire made conversation impossible.\nA merchant\'s messenger scurried by with a handful of accounts'
# c31 = '"\nPiling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone'
# c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."\n\n\n\n\n\n\n\n\n\nMapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'
#
# c_0 = 'One\n\n\n\n\n\n\n“Ilsabet, wake up!”\nIlsabet pulled the down-filled covers tighter around her thin body and ignored her maidservant’s call.\n“You were up half the night writing in that journal, weren’t you?”\nGreta, Ilsabet’s maid, could sign her name in a beautiful script, but that was all'
# c_1 = 'Reading, writing, even contemplative thought seemed beyond her reach. But she was a practical and caring woman, and Ilsabet ignored the shortcomings. “No,” she replied. “I just couldn’t sleep.”\nInstead, Ilsabet had gone to Lord Jorani’s chambers in the highest room in the castle tower'
#

def add_space_after_nth_newline_block(text, n, min_newlines=3):
    """
    Adds a space after the nth occurrence of a block of consecutive newlines
    (with a minimum specified) in the text.

    Args:
        text (str): The input text.
        n (int): The occurrence number of the newline block to modify (1-based index).
        min_newlines (int): The minimum number of consecutive newlines to define a block.

    Returns:
        str: The modified text with a space added after the specified newline block.
    """
    # Define the pattern: block of at least 'min_newlines' consecutive newlines
    pattern = rf'(\n{{{min_newlines},}})(?! )'

    # Find all matches of the pattern
    matches = list(re.finditer(pattern, text))

    # Check if the nth occurrence exists
    if n <= len(matches):
        # Get the start and end positions of the nth match
        start, end = matches[n - 1].span()
        # Insert a space after the newline block
        text = text[:end] + ' ' + text[end:]

    return text

def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    - Example: Replace sequences of 4+ newlines with 'New section - '.
    """
    return re.sub(r'\n{4,}', ' New section - ', chunk)


def process_comma_quote(text):
    """
    Replaces occurrences of a comma immediately followed by a double quote
    (standard or typographic) with the double quote followed by a comma.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with ',<quote>' replaced by '<quote>,'.
    """
    # Define the pattern: comma followed by any double quote character
    pattern = r',([“”"])'
    # Replace the pattern with the quote followed by a comma
    return re.sub(pattern, r'\1,', text)


def process_period_quote(text):
    """
    Replaces occurrences where a period immediately precedes a double quote
    (standard or typographic) with the double quote followed by the period.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with '<period><quote>' replaced by '<quote><period>'.
    """
    # Define the pattern: period followed by any double quote character
    pattern = r'\.([“”"])'
    # Replace the pattern with the quote followed by the period
    return re.sub(pattern, r'\1.', text)

# text = '"No,"'
# text2 = '"No."'
#
# out4 = process_comma_quote(text)
# out5 = process_period_quote(text2)


def process_quote_newline_quote(input_text):
    """
    Replaces instances of a double quote (standard or typographic) followed by a newline character
    and another double quote with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    # Match ASCII or typographic quotes followed by a newline and another quote
    pattern = r'([“”"])\n([“”"])'
    # Replace the pattern with a single space
    return re.sub(pattern, ' "', input_text)


# out6 = process_quote_newline_quote(c5)
# out = process_quote_newline_quote('the table."\n"I\'m busy')


def process_quote_newlines_letter(text):
    """
    Replaces occurrences of a double quote (standard or typographic) followed by one or more newline characters
    and a letter with the double quote followed by a space and the letter.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific patterns replaced.
    """
    # Define the pattern: double quote (standard or typographic) followed by one or more newline characters and a letter
    pattern = r'([“”"])\r?\n{1,2}([a-zA-Z])'
    # Replace the pattern with double quote followed by a space and the letter
    return re.sub(pattern, r'\1 \2', text)

#
# out = process_quote_newlines_letter(c0)
#
# text = '"\nPiling her parcels in a dry space, the assistant joined Myrthin'
# out = process_quote_newlines_letter(text)
# tts.tts_to_file(text=out, speaker_wav="/home/nim/Documents/ralph_lister.wav", language="en", file_path="/home/nim/TRY.wav")
#


def process_quote_newline(text):
    """
    Replaces occurrences of a double quote (standard or typographic) followed by a newline character
    with the double quote, a space, and a newline.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific patterns replaced.
    """
    # Define the pattern: double quote (standard or typographic) followed by newline
    pattern = r'([“”"])\n'
    # Replace the pattern with the double quote followed by a space and newline
    return re.sub(pattern, r'\1 ', text)

# text = '"\nPiling her parcels in a dry space, the assistant joined Myrthin'
# out = process_quote_newline(text)
#
# out3 = process_quote_newline(c5)
# print(out3)


def process_newlines_quote(text):
    """
    Replaces occurrences of one or two newline characters followed by a double quote
    (standard or typographic) with a space followed by the double quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with the specified patterns replaced.
    """
    # Define the pattern: one or two newline characters followed by a double quote
    pattern = r'\n{1,2}([“”"])'
    # Replace the pattern with a space followed by the matched double quote
    return re.sub(pattern, r' \1', text)

# text = 'And all.\n\n"\Piling her parcels in a dry space, the assistant joined Myrthin'
# out3 = process_newlines_quote(text)
# print(out3)


# out = process_newlines_quote(c0)
# print(out)
# tts.tts_to_file(text=out, speaker_wav="/home/nim/Documents/ralph_lister.wav", language="en", file_path="/home/nim/TRY.wav")
#
# text = '\nShe hesitated, then said, “Very well, but it comes off before we reach my father’s camp.”\nThey rode in silence through the fields, fallow in late autumn, Jorani constantly scanning the countryside, alert for an ambush. At the edge of the forest road, he reined in his horse and gave three loud whistles. A handful of soldiers rode toward them'
# out = process_quote_newlines_letter(text)
# tts.tts_to_file(text=out, speaker_wav="/home/nim/Documents/ralph_lister.wav", language="en", file_path="/home/nim/TRY.wav")
#
#
# text = 'A love,\n"A'
# out = process_newlines_quote(text)


def process_comma_newline_quote(text):
    """
    Replaces occurrences of a comma followed by a newline character and a double quote
    (standard or typographic) with a comma, a space, and the double quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with ',\n"' patterns replaced by ', "'.
    """
    # Define the pattern: comma followed by optional carriage return, newline, and a double quote
    pattern = r',\r?\n([“”"])'
    # Replace the pattern with comma, space, and the double quote
    return re.sub(pattern, r', \1', text)

# text4 = 'A love,\n"And'
# out = process_comma_newline_quote(text4)


def process_comma_newline_letter(text):
    """
    Replaces occurrences of a comma followed by exactly one newline character and a letter,
    or a comma followed by exactly one newline character and a quote (standard or typographic),
    with the comma followed by a space and the letter or quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with ',\n<letter>' or ',\n<quote>' replaced by ', <letter>' or ', <quote>'.
    """
    # Define the pattern: comma followed by optional carriage return and a single newline, then a letter or quote
    pattern = r',\r?\n([a-zA-Z“”"])'
    # Replace the pattern with comma followed by a space and the letter or quote
    return re.sub(pattern, r', \1', text)

# text= 'A love,\nA'
# out = process_comma_newline_letter(text)


# might be required to adjust when paragraphs have more (\n)s
def process_period_newlines_quote(text):
    """
    Replaces occurrences of a period followed by one or two newlines and a double quote
    (standard or typographic) with the period followed by a space and the double quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific patterns replaced.
    """
    # Define the pattern: period followed by one or two newlines and a double quote
    pattern = r'\.\n{1,2}([“”"])'
    # Replace the pattern with period followed by a space and the double quote
    return re.sub(pattern, r'. \1', text)

# text5 = 'floor.\n"The mage finally grunted'
# text5 = 'floor.\n\n"The mage finally grunted'
# out5 = process_period_newlines_quote(text5)


# might be required to adjust when paragraphs have more (\n)s
def process_period_newlines_letter(text):
    """
    Replaces occurrences of a period followed by one or two newlines and a single letter
    with the period followed by a space and the letter.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific newlines replaced.
    """
    # Define the pattern: period followed by one or two newlines and a single letter
    pattern = r'\.\n{1,2}([a-zA-Z])'
    # Replace the pattern with period followed by a space and the letter
    return re.sub(pattern, r'. \1', text)

# text3 = 'A love.\nA'
# text3 = 'A love.\n\nA'
# out3 = process_period_newlines_letter(text3)


# might be required to adjust when paragraphs have more (\n)s
def process_period_newlines(text):
    """
    Replaces occurrences of a period followed by one or two newline characters,
    optionally followed by a quote (standard or typographic), with a period,
    a space, and the quote if present.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with '.\n', '.\n\n', '.\n"', '.\n\n"', '.\n“', etc.,
             replaced by '. ', '. "', '. “', etc.
    """
    # Define the pattern: period followed by one or two newline sequences,
    # optionally followed by a quote character
    pattern = r'\.(\r?\n){1,2}([“”"])?'
    # Replace the pattern with period, space, and the optional quote
    return re.sub(pattern, lambda m: '. ' + (m.group(2) or ''), text)


# text4 = 'floor.\n\nThe mage finally grunted'
# text5 = 'floor.\nThe mage finally grunted'
# text6 = 'floor.\n\n"The mage finally grunted'
#
# out4 = process_period_newlines(text4)
# out5 = process_period_newlines(text5)
# out6 = process_period_newlines(text6)




def process_text(text):
    """
    Calls all text processing functions in a specified order.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The processed text after all transformations.
    """
    # Apply all transformations in the specified order
    text = process_comma_quote(text)
    text = process_period_quote(text)
    text = process_quote_newline_quote(text)
    text = process_quote_newlines_letter(text)
    text = process_quote_newline(text)
    text = process_newlines_quote(text)
    text = process_comma_newline_quote(text)
    text = process_comma_newline_letter(text)
    text = process_period_newlines_quote(text)
    text = process_period_newlines_letter(text)
    text = process_period_newlines(text)
    return text