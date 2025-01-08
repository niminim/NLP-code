import os


def save_text_chunk(texts_folder, chapter_name_adj, chunk, idx):
    chapter_text_dir = os.path.join(texts_folder, chapter_name_adj)
    os.makedirs(chapter_text_dir, exist_ok=True)
    text_file_path = os.path.join(texts_folder, chapter_name_adj ,f"part{idx + 1}.txt")
    with open(text_file_path, "w") as text_file:
        text_file.write(chunk)