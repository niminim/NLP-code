import os


def create_dirs(base, book_name, ref, chunk_size):
    book_name = 'Baroness_of_Blood2' + f"_by_{ref}_{chunk_size}"
    book_path = os.path.join(base, book_name)

    # Create "texts" folder
    texts_folder = os.path.join(book_path, "text_chunks")
    os.makedirs(texts_folder, exist_ok=True)

    return  book_path, texts_folder


