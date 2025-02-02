import os
import re

# Locate chapters

# Find all occurrences of chapters
# def find_chapter_locations(text, chapters):
#     results = {}
#
#     for chapter in chapters:
#         # Match chapter titles preceded and followed by newlines
#         pattern = rf'(?<!\S){re.escape(chapter)}(?!\S)'  # Matches standalone words, avoiding word boundaries (is more flexible for in-line standalone matches
#
#         matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]
#
#         # Store the results for each chapter in a dictionary
#         results[chapter] = matches
#
#     return results


# For Dragons of Krynn
def find_chapter_locations_full_block(text, chapters):
    """
    Finds all occurrences of chapter titles in the text where:
    - The chapter title is preceded by more than 3 newline characters.
    - The chapter title is followed by exactly 1 newline.

    Captures the entire block including the preceding and following newlines.

    Args:
        text (str): The input text to search.
        chapters (list of str): A list of chapter titles to look for.

    Returns:
        list: A list of tuples in the format [('Chapter Name', (start, end))].
    """
    results = []

    for chapter in chapters:
        # Pattern to match the chapter name with specified newline conditions
        pattern = rf'(\n{{3,}}){re.escape(chapter)}(\n)'

        # Find all matches including the newline blocks and chapter name
        matches = [(match.start(0), match.end(0)) for match in re.finditer(pattern, text)]

        # Add chapter name and its positions to the results
        for start, end in matches:
            results.append((chapter, (start, end)))

    return results


# For Baroness of Blood (and other ravenloft books)
def find_chapter_locations_full_block2(text, chapters):
    """
    Finds all occurrences of chapter titles in the text where:
    - The chapter title is surrounded by blocks of newlines.
    - Captures the entire block of newlines along with the chapter title.

    Returns results as a list of tuples in the format: [('Chapter Name', (start, end))].

    Args:
        text (str): The input text to search.
        chapters (list of str): A list of chapter titles to look for.

    Returns:
        list: A list of tuples where each tuple contains the chapter title and its (start, end) positions.
    """
    results = []

    for chapter in chapters:
        # Pattern to match entire newline block, including the chapter title
        pattern = rf'(\n+){re.escape(chapter)}(\n{{3,}})'

        # Find all matches and include entire match (newlines + chapter title)
        matches = [(match.start(0), match.end(0)) for match in re.finditer(pattern, text)]

        # Add chapter name and its positions to the results
        for start, end in matches:
            results.append((chapter, (start, end)))

    return results


# We need it if chapters are not organized by order
def get_chapter_text(epub_content, chapters_dict, chapters, chapter_idx):
    # the function gets the chapters list and the chapter idx and return the corresponding text
    chapter_info = chapters_dict[chapters[chapter_idx]]
    chapter_start = chapter_info['name_start']
    chapter_end = chapter_info['chapter_end']
    chapter_text = epub_content[chapter_start:chapter_end]
    chapter_text = chapter_text + '.'
    print(chapter_text)
    return chapter_text, chapter_info



# Sort chapters by their starting position
def sort_chapters_by_position(chapter_locations):
    """
    Sorts a list of chapter occurrences by their starting positions.

    Args:
        chapter_locations (list): A list of tuples in the form [('Chapter Name', (start, end)), ...].

    Returns:
        list: A sorted list of tuples by the starting position.
    """
    return sorted(chapter_locations, key=lambda x: x[1][0])


def create_chapters_dict(sorted_chapters, epub_content):
    # the function creates a dictionary with starts and beginings of each chapter
    chapters_dict = {}
    for i, chapter_data in enumerate(sorted_chapters):
        if i < len(sorted_chapters) - 1:

            chapters_dict[chapter_data[0]] = {'name': epub_content[chapter_data[1][0]: chapter_data[1][1]],
                                              'name_start': chapter_data[1][0],
                                              'name_end': chapter_data[1][1],
                                              'chapter_end': sorted_chapters[i + 1][1][0] - 1,
                                              'length': sorted_chapters[i + 1][1][0] - 1 - chapter_data[1][0]
                                              }
        else:
            chapters_dict[chapter_data[0]] = {'name': epub_content[chapter_data[1][0]: chapter_data[1][1]],
                                              'name_start': chapter_data[1][0],
                                              'name_end': chapter_data[1][1],
                                              'chapter_end': len(epub_content),
                                              'length':  len(epub_content) - chapter_data[1][0]
                                              }

    return chapters_dict

##### End of Locate chapters
