import re

######## Clean text

# To tackles first chpater name followed by a block of \n with no whitespace between the text
def add_space_after_first_newline_block(text):
    """
    Adds a whitespace after the first occurrence of 3 or more newlines in the text.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with a space added after the first block of 3 or more newlines.
    """
    # Match the first occurrence of 3 or more newlines
    pattern = r'(\n{3,})(?! )'

    # Add a space after the newline block
    modified_text = re.sub(pattern, r'\1 ', text, count=1)

    return modified_text


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


def fix_punctuation_spacing(text):
    """
    Replaces:
    - All occurrences of '."' with '".' in the input text.
    - All occurrences of ',"' with '",' in the input text.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with corrected punctuation.
    """
    # Replace '."' with '".'
    text = text.replace('."', '".')
    # Replace ',"' with '",'
    text = text.replace(',"', '",')
    return text

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