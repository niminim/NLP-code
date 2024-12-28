import re

def replace_newline_sequences(input_text):
    """
    Replace 3 or more newline characters with "  An ornamental break  ."
    """
    return re.sub(r'\n{3,}', '  ', input_text)

def process_chunk_add_new_section(chunk):
    """
    Cleans a single text chunk by applying specific transformations.
    Replace sequences of 5+ newlines with 'New section - '.
    """
    return re.sub(r'\n{4,}', ' New section - ', chunk)

def process_chunk_replace_quotes_newline(input_text):
    """
    Replaces instances of '"' followed by '\n' followed by '"' with a single space.
    """
    return re.sub(r'"\n"', '" "', input_text)

def replace_right_quote_newline(input_text):
    """
    Replaces instances of '”\n' with a single space.
    """
    return re.sub(r'”\n', ' ', input_text)

def process_chunk_replace_quotes_newlines(input_text):
    """
    Replaces instances of '"' followed by one or more '\n' characters followed by '"' with a single space.
    """
    return re.sub(r'"\n{1,}"', '" "', input_text)

def replace_newline_after_quote(input_text):
    """
    Replaces instances of '"\n' followed by a capital letter with '" '
    and retains the capital letter.
    """
    return re.sub(r'"\n([A-Z])', r'" \1', input_text)