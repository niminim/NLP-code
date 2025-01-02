import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def read_epub(file_path):
    # Function reads the EPUB content
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