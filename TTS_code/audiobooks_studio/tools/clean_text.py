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

# def fix_punctuation_with_qoute(text):
#     """
#     Replaces:
#     - All occurrences of '."' with '".' in the input text.
#     - All occurrences of ',"' with '",' in the input text.
#
#     Args:
#         text (str): The input text.
#
#     Returns:
#         str: The modified text with corrected punctuation.
#     """
#     # Replace '."' with '".'
#     text = text.replace('."', '".')
#     # Replace ',"' with '",'
#     text = text.replace(',"', '",')
#     return text


def fix_punctuation_with_quote(text):
    """
    Adjusts the placement of commas and periods relative to quotation marks in the text.
    Specifically:
    - Replaces instances of ',"' with '",'.
    - Replaces instances of '."' with '".'.

    Args:
        text (str): The input text.

    Returns:
        str: The text with corrected punctuation placement.
    """
    # Replace ',"' with '",'
    text = re.sub(r'(\w),”', r'\1”,', text)
    # Replace '."' with '".'
    text = re.sub(r'(\w)\.”', r'\1”.', text)
    return text


def replace_period_newline(text):
    """
    Replaces occurrences of a period followed by a newline character with just a period.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with '.\n' replaced by '.'.
    """
    # Use re.sub to replace '.\n' with '.'
    return re.sub(r'\.\n', '. ', text)


def replace_newline_after_quote(text):
    """
    Replaces occurrences where a quotation mark followed by a period and a newline,
    or just a newline, is immediately followed by a capital letter. The newline is replaced with a space.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with specific newlines replaced by spaces.
    """
    # Pattern to match '."\\n' or '"\\n' followed by a capital letter
    pattern = r'([”"]\.)?\n([A-Z])'
    # Replace the matched pattern by removing the newline and adding a space
    return re.sub(pattern, lambda m: (m.group(1) or '') + ' ' + m.group(2), text)


def add_space_after_newlines_with_typographic_quote_and_capital(text):
    """
    Adds a space after one or more newlines followed by a quote (ASCII or typographic) and a capital letter.

    Args:
        text (str): The input text.

    Returns:
        str: The modified text with a space added after the newline block.
    """
    # Match one or more newlines followed by a quote (ASCII or typographic) and a capital letter
    pattern = r'(\n+)([“"])([A-Z])'
    # Add a space after the newline block
    modified_text = re.sub(pattern, r'\1 \2\3', text)
    return modified_text




def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    - Example: Replace sequences of 4+ newlines with 'New section - '.
    """
    return re.sub(r'\n{4,}', ' New section - ', chunk)


# Tacles "\n"
# def process_chunk_replace_quotes_newline(input_text):
    # """
    # Replaces instances of '"' followed by '\n' followed by '"' with a single space.
    #
    # Args:
    #     input_text (str): The input text.
    #
    # Returns:
    #     str: The text with the pattern replaced by a single space.
    # """
    # return re.sub(r'"\n"', '" "', input_text)

def process_chunk_replace_quotes_newline(input_text):
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


#
# def process_chunk_replace_quotes_newlines(input_text):
#     """
#     Replaces instances of '"' followed by one or more '\n' characters followed by '"' with a single space.
#
#     Args:
#         input_text (str): The input text.
#
#     Returns:
#         str: The text with the pattern replaced by a single space.
#     """
#     return re.sub(r'"\n{1,}"', '" "', input_text)

def process_chunk_replace_quotes_newlines(input_text):
    """
    Replaces instances of a quote (ASCII or typographic) followed by one or more '\n' characters
    followed by another quote with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced by a single space.
    """
    # Match ASCII or typographic quotes around one or more newlines
    return re.sub(r'([“"])\\n{1,}([“"])', r'\1 \2', input_text)



# def replace_right_quote_newline(input_text):
#     """
#     Replaces instances of '”\n' with a single space.
#
#     Args:
#         input_text (str): The input text.
#
#     Returns:
#         str: The text with the pattern replaced.
#     """
#     return re.sub(r'”\n', ' ', input_text)

def replace_right_quote_newline(input_text):
    """
    Replaces instances of '”\n' or '”\n{1,}' (one or more newlines) with a single space.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    # Match a typographic right quote followed by one or more newline characters
    return re.sub(r'”\n{1,}', '” ', input_text)


# def replace_newline_after_quote(input_text):
#     """
#     Replaces instances of '"\n' followed by a capital letter with '" '
#     and retains the capital letter.
#
#     Args:
#         input_text (str): The input text.
#
#     Returns:
#         str: The text with the pattern replaced.
#     """
#     return re.sub(r'"\n([A-Z])', r'" \1', input_text)


def replace_newline_after_quote(input_text):
    """
    Replaces instances of '"' followed by a newline and then a capital letter
    with '" ' (adding a space instead of the newline) and retains the capital letter.

    Args:
        input_text (str): The input text.

    Returns:
        str: The text with the pattern replaced.
    """
    # Match a straight quote, followed by a newline, and then a capital letter
    return re.sub(r'"\n+([A-Z])', r'" \1', input_text)






def process_and_fix_text(input_text):
    """
    Processes the input text to:
    1. Replace instances of '"' followed by '\n' followed by '"' with a single space.
    2. Replace instances of '"' followed by one or more '\n' characters followed by '"' with a single space.
    3. Replace instances of '”\n' with a single space.
    4. Replace instances of '"\n' followed by a capital letter with '" ' (retaining the capital letter).
    5. Replace all occurrences of '."' with '".'.
    6. Replace all occurrences of ',"' with '",'.

    Args:
        input_text (str): The input text.

    Returns:
        str: The processed text with all patterns replaced.
    """
    # Replace '"' followed by '\n' followed by '"'
    input_text = re.sub(r'"\n"', '" "', input_text)

    # Replace '"' followed by one or more '\n' characters followed by '"'
    input_text = re.sub(r'"\n{1,}"', '" "', input_text)

    # Replace '”\n' with a single space
    input_text = re.sub(r'”\n', ' ', input_text)

    # Replace '"\n' followed by a capital letter with '" '
    input_text = re.sub(r'"\n([A-Z])', r'" \1', input_text)

    # Replace '."' with '".'
    input_text = input_text.replace('."', '".')

    # Replace ',"' with '",'
    input_text = input_text.replace(',"', '",')

    return input_text


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