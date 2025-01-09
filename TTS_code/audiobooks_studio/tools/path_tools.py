import os


def create_dirs(base, book_name, ref, chunk_size):
    book_name = book_name + f"_by_{ref}_{chunk_size}"
    book_path = os.path.join(base, book_name)

    # Create "texts" folder
    texts_folder = os.path.join(book_path, "texts")
    os.makedirs(texts_folder, exist_ok=True)

    audio_dir = os.path.join(book_path, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    text_chunks_dir = os.path.join(texts_folder, 'orig_chunks')
    text_transcriptions_dir = os.path.join(texts_folder, 'transcriptions')
    os.makedirs(text_chunks_dir, exist_ok=True)
    os.makedirs(text_transcriptions_dir, exist_ok=True)

    return  book_path, audio_dir, text_chunks_dir, text_transcriptions_dir


