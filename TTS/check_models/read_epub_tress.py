import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re


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


# Function to find all occurrences of chapters
def find_chapter_locations(text, chapters):
    results = {}

    # Loop through each chapter title
    for chapter in chapters:
        # Use re.finditer to find all occurrences of the chapter
        matches = [(match.start(), match.end()) for match in re.finditer(re.escape(chapter.upper()), text)]

        # Store the results for each chapter in a dictionary
        results[chapter] = matches

    return results


# List of chapters to find
chapters = ['The Girl', 'The Groundskeeper', 'The Duke', 'The Son', 'The Bride',
            'The Inspector', 'The Father', 'The Stowaway', 'The Rat'] # The chapters are with all capitals, thus using .upper() in function
parts = ['PART ONE', 'PART TWO', 'PART THREE', 'PART FOUR', 'PART FIVE', 'PART SIX']

# Find all locations of chapter titles
parts_locations = find_chapter_locations(epub_content, parts)
chapter_locations = find_chapter_locations(epub_content, chapters)

# Print the part locations
for part, locations in parts_locations.items():
    print(f"'{part}' found at positions: {locations}")

# Print the chapter locations
for chapter, locations in chapter_locations.items():
    print(f"'{chapter}' found at positions: {locations}")


for i, chapter in enumerate(chapters):

    chapter_start = chapter_locations[chapter][0][0]

    if i < len(chapters)-1:
        chapter_end = chapter_locations[chapters[i+1]][0][0]-1
    elif i == len(chapters)-1:
        chapter_end = chapter_start + 20

    print(f"chapter {chapter} - start {chapter_start}, end {chapter_end}, (length={chapter_end - chapter_start})")


chapter_start = chapter_locations['The Girl'][0][0]
chapter_end = chapter_locations['The Girl'][0][1]+50
first_chapter = epub_content[chapter_start:chapter_end]
print(first_chapter)
text = first_chapter


part_start = parts_locations['PART ONE'][0][0]
part_end = parts_locations['PART ONE'][0][1]
first_part = epub_content[part_start:part_end]
print(first_part)
text = first_part