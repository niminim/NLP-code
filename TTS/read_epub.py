import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


# Function to read the EPUB content
def read_epub(file_path):
    book = epub.read_epub(file_path)

    # To store all the text content from the EPUB
    all_text = []

    # Iterate over the book items
    for item in book.get_items():
        # Only extract the documents that are of type XHTML
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Use BeautifulSoup to extract text from the HTML content
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            all_text.append(soup.get_text())

    return '\n'.join(all_text)


# Path to your EPUB file
file_path = '/home/nim/Downloads/Tress_of_the_Emerald_Sea_by_Brandon_Sanderson.epub'

# Reading the EPUB file
epub_content = read_epub(file_path)

# Print a portion of the EPUB content
print(epub_content[0:2000])  # Print the first 1000 characters

import re

# List of chapters to find
chapters = ['The Girl', 'The Groundskeeper', 'The Duke']
parts = ['PART ONE', 'PART TWO', 'PART THREE', 'PART FOUR', 'PART FIVE', 'PART SIX']

# Function to find all occurrences of chapters
def find_chapter_locations(text, chapters):
    results = {}

    # Loop through each chapter title
    for chapter in chapters:
        # Use re.finditer to find all occurrences of the chapter
        matches = [(match.start(), match.end()) for match in re.finditer(re.escape(chapter), text)]

        # Store the results for each chapter in a dictionary
        results[chapter] = matches

    return results


# Find all locations of chapter titles
chapter_locations = find_chapter_locations(epub_content, chapters)

# Print the locations
for chapter, locations in chapter_locations.items():
    print(f"'{chapter}' found at positions: {locations}")


chapter_start = 6650
chapter_end = 12570
first_chapter = epub_content[chapter_start:chapter_end]
print(first_chapter)
text = first_chapter