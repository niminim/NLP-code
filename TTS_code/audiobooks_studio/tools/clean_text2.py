import re
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


c0 =  'Scourge of the Wicked Kendragon\nJanet Pack\n\n\n\n\n\n\n"But I was only… aaahhhh!"\nPropelled by the shopkeeper\'s arm, the kender Mapshaker Wanderfuss became a bird, sailing through the door and thudding into the middle of Daltigoth\'s main street. Dust clouded around the kender. Indignant and coughing, he levered himself to a sitting position'
c5 = '" Mapshaker wandered into the forge area and continued his explanation. "I only tasted it. After all, one corner was hanging over the edge of the table."\n"I\'m busy. Go away," the smith said roughly, pumping the bellows until the roaring fire made conversation impossible.\nA merchant\'s messenger scurried by with a handful of accounts'
c31 = '"\nPiling her parcels in a dry space, the assistant joined Myrthin, eyes searching the wooden floor.\nThe mage finally grunted in satisfaction and straightened, a tiny scale from the brass dragon balanced on the tip of one crooked finger. "Get someone to patch the roof well enough so the rest of the house won\'t flood while I\'m gone'
c33 = '" He turned toward his workroom, the precious dragon scale imprisoned between gnarled thumb and forefinger. "Get to work, Kharian. Now."\n\n\n\n\n\n\n\n\n\nMapshaker\'s eyes were closed. He felt much cooler than he had a few minutes ago. Wind tickled his ears and soothed the fire streaking throughout his body. He relaxed'

c_0 = 'One\n\n\n\n\n\n\n“Ilsabet, wake up!”\nIlsabet pulled the down-filled covers tighter around her thin body and ignored her maidservant’s call.\n“You were up half the night writing in that journal, weren’t you?”\nGreta, Ilsabet’s maid, could sign her name in a beautiful script, but that was all'
c_1 = 'Reading, writing, even contemplative thought seemed beyond her reach. But she was a practical and caring woman, and Ilsabet ignored the shortcomings. “No,” she replied. “I just couldn’t sleep.”\nInstead, Ilsabet had gone to Lord Jorani’s chambers in the highest room in the castle tower'



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

text = '"No,"'
text2 = '"No."'

out4 = process_comma_quote(text)
out5 = process_period_quote(text2)


def process_quote_newlines_letter(text):
    """
    Replaces occurrences of a double quote (standard or typographic) followed by one or two newline characters and a letter
    with the double quote directly followed by the letter.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific patterns replaced.
    """
    # Define the pattern: double quote (standard or typographic) followed by one or two newlines and a letter
    pattern = r'([“”"])\n{1,2}([a-zA-Z])'
    # Replace the pattern with double quote followed by the letter
    return re.sub(pattern, r'\1\2', text)


out = process_quote_newlines_letter(c0)

text = '"\nPiling her parcels in a dry space, the assistant joined Myrthin'
out = process_quote_newlines_letter(text)
tts.tts_to_file(text=out, speaker_wav="/home/nim/Documents/ralph_lister.wav", language="en", file_path="/home/nim/TRY.wav")

text = '”\nShe hesitated, then said, “Very well, but it comes off before we reach my father’s camp.”\nThey rode in silence through the fields, fallow in late autumn, Jorani constantly scanning the countryside, alert for an ambush. At the edge of the forest road, he reined in his horse and gave three loud whistles. A handful of soldiers rode toward them'
out = process_quote_newlines_letter(text)


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
    return re.sub(pattern, r'\1 \n', text)



out3 = process_quote_newline(c5)
print(out3)


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

text3 = 'A love.\nA'
text3 = 'A love.\n\nA'
out3 = process_period_newlines_letter(text3)

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

text= 'A love,\nA'
out = process_comma_newline_letter(text)


def process_newline_quote(text):
    """
    Replaces occurrences of a newline character followed by a double quote
    (standard or typographic) with a space followed by the double quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with '\n' followed by a quote replaced by ' ' followed by the quote.
    """
    # Define the pattern: newline followed by any double quote character
    pattern = r'\n([“”"])'
    # Replace the pattern with space followed by the matched quote character
    return re.sub(pattern, r' \1', text)

out = process_newline_quote(c0)
print(out)
tts.tts_to_file(text=out, speaker_wav="/home/nim/Documents/ralph_lister.wav", language="en", file_path="/home/nim/TRY.wav")

text = 'A love,\n"A'


def process_quote_newline_quote(input_text):
    """
    Replaces instances of a quote (ASCII or typographic) followed by '\n'
    followed by another quote with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    # Match ASCII or typographic quotes around a newline
    return re.sub(r'([“"])\\n([“"])', r'\1 \2', input_text)


out = process_quote_newline_quote('the table."\n"I\'m busy')


out6 = process_quote_newline_quote(c5)


def process_comma_newline_letter(text):
    """
    Replaces occurrences of a comma followed by exactly one newline character and a letter or quote
    with the comma followed by a space and the letter or quote.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with ',\n<letter_or_quote>' (or ',\r\n<letter_or_quote>') replaced by ', <letter_or_quote>'.
    """
    # Define the pattern: comma followed by optional carriage return, a single newline, and a letter or quote
    pattern = r',\r?\n([a-zA-Z“”"])'
    # Replace the pattern with comma followed by a space and the letter or quote
    return re.sub(pattern, r', \1', text)

text4 = 'A love,\nA'
out = process_comma_newline_letter(text4)


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

text4 = 'A love,\n"And'
out = process_comma_newline_quote(text4)



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

text5 = 'floor.\n"The mage finally grunted'
text5 = 'floor.\n\n"The mage finally grunted'
out5 = process_period_newlines_quote(text5)


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


text6 = 'floor.\n\nThe mage finally grunted'
text6 = 'floor.\nThe mage finally grunted'
text6 = 'floor.\n\n"The mage finally grunted'

out6 = process_period_newlines(text6)


def combined_text_processor(text):
    """
    Applies a series of text processing transformations to the input text in the following order:
    1. Replaces occurrences of a comma immediately followed by a double quote with a double quote followed by a comma.
    2. Replaces occurrences where a period immediately precedes a double quote with the double quote followed by the period.
    3. Replaces occurrences of a double quote followed by a newline and a letter with the double quote directly followed by the letter.
    4. Replaces occurrences of a newline character followed by a double quote with a space followed by a double quote.
    5. Replaces occurrences of a double quote followed by a newline character with a double quote, space, and newline.
    6. Replaces instances of a quote (ASCII or typographic) followed by '\n' followed by another quote with a single space.
    7. Replaces occurrences of a comma followed by a newline and a single letter with the comma followed by a space and the letter.
    8. Replaces occurrences of a period followed by one or two newlines and a single letter with the period followed by a space and the letter.
    9. Replaces occurrences of a period followed by one or two newlines and a double quote with the period followed by a space and the double quote.
    10. Replaces occurrences of a period followed by a newline with the period followed by a space.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text after applying all transformations.
    """
    # 1. Replace ',"' with '",'
    text = re.sub(r',"', '",', text)

    # 2. Replace '."' with '".'
    text = re.sub(r'\.(")', r'\1.', text)

    # 3. Replace '"\n' followed by a letter with '"' and the letter
    text = re.sub(r'"\n([a-zA-Z])', r'"\1', text)

    # 4. Replace '\n"' with ' "'
    text = re.sub(r'\n"', ' "', text)

    # 5. Replace '"\n' with '" \n'
    text = re.sub(r'"\n', '" \n', text)

    # 6. Replace quote followed by '\n' followed by another quote with a single space
    text = re.sub(r'([“"])\\n([“"])', r'\1 \2', text)

    # 7. Replace ',\n' followed by a letter with ', ' and the letter
    text = re.sub(r',\n([a-zA-Z])', r', \1', text)

    # 8. Replace '.\n' (one or two newlines) followed by a letter with '. ' and the letter
    text = re.sub(r'\.\n{1,2}([a-zA-Z])', r'. \1', text)

    # 9. Replace '.\n' (one or two newlines) followed by a double quote with '. "'
    text = re.sub(r'\.\n{1,2}"', '. "', text)

    # 10. Replace '.\n' with '. '
    text = re.sub(r'\.\n', '. ', text)

    return text