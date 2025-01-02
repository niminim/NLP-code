import re

def efficient_split_text_to_chunks(text, max_length): # this was used and worked
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