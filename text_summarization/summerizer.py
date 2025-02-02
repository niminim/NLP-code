import torch
from transformers import pipeline

device = "cuda" if torch.cuda.is_available() else "cpu"

summarizer = pipeline("summarization", device=device)
#################################

import nltk
from transformers import pipeline

# Download the Punkt tokenizer for sentence splitting
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to chunk text while preserving sentences
def chunk_text(text, max_tokens=500):
    sentences = sent_tokenize(text)  # Split text into sentences
    chunks, current_chunk = [], []
    current_length = 0

    for sentence in sentences:
        token_count = len(sentence.split())  # Estimate token count
        if current_length + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))  # Save current chunk
            current_chunk, current_length = [], 0  # Reset chunk
        current_chunk.append(sentence)
        current_length += token_count

    if current_chunk:  # Add the last chunk
        chunks.append(" ".join(current_chunk))

    return chunks


############ Extract full text
import os
import re

folder = '/home/nim/Mithras_Court_by_scott_brick_250/texts/orig_chunks/Chapter_One'


# List all .txt files
files = [f for f in os.listdir(folder) if f.endswith(".txt")]

# Sort using numerical order extracted from filenames
sorted_files = sorted(files, key=lambda x: int(re.search(r'\d+', x).group()))

print(sorted_files)  # ['part1.txt', 'part2.txt', 'part3.txt']


# Concatenate file contents
full_text = ""

for file in sorted_files:
    file_path = os.path.join(folder, file)
    with open(file_path, "r", encoding="utf-8") as f:
        full_text += f.read() + "\n\n"  # Add spacing between parts

# Print or save the concatenated text
print(full_text)  # Print to console (or use below to save)

# Save to a new file
output_file = os.path.join('/home/nim/Mithras_Court_by_scott_brick_250/', "full_text_chapter1.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(full_text)
print(f"Combined text saved to {output_file}")
############ End of Extract full text


############ Summarize the full text

# Chunk text without splitting sentences
chunks = chunk_text(full_text, max_tokens=768)

def complete_summary(text):
    sentences = sent_tokenize(text)
    if len(sentences) > 1:
        return " ".join(sentences[:-1])  # Remove incomplete last sentence
    return text  # Return as is if it's already a single sentence

# Summarize each chunk
summaries = [summarizer(chunk, max_new_tokens=100, min_length=60, do_sample=False)[0]["summary_text"] for chunk in chunks]

summaries = [complete_summary(summarizer(chunk, max_new_tokens=80, min_length=60, do_sample=False)[0]["summary_text"]) for chunk in chunks]

# Combine summarized chunks
final_summary = " ".join(summaries)

print(final_summary)
############ End of summary


############ TTS for hte summary
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


folder = '/home/nim/Mithras_Court_by_scott_brick_250'
for idx, summary in enumerate(summaries):
    print(idx)
    tts.tts_to_file(text=summary, speaker_wav="/home/nim/Documents/scott_brick.wav", language="en", file_path=f"{folder}/summary_{idx}.wav")

############


















#########################

import nltk
from transformers import pipeline

# Download the Punkt tokenizer for sentence splitting
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to chunk text while preserving sentences
def chunk_text(text, max_tokens=500):
    sentences = sent_tokenize(text)  # Split text into sentences
    chunks, current_chunk = [], []
    current_length = 0

    for sentence in sentences:
        token_count = len(sentence.split())  # Estimate token count
        if current_length + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))  # Save current chunk
            current_chunk, current_length = [], 0  # Reset chunk
        current_chunk.append(sentence)
        current_length += token_count

    if current_chunk:  # Add the last chunk
        chunks.append(" ".join(current_chunk))

    return chunks

# Example long text
long_text = """Uff it's been such a long time since I have been this satisfied with romantasy which also had like 600+ pages and like I wasnt bored for a single second, I binged this every chance I got. Usually when I read a romantasy or a fantasy im more interested in the plot or the storyline which was very prominent in this book however the romance swept me off my feet 🤭 maybe because it was a love triangle(ish) and I got my way 🤭 but honestly it was so well written that i'm shocked at how no ones raving about this book because it's easy to read, gripping, angsty with fun banter and of course Viking inspired so like?? what are you guys actually waiting for?? because I'll be diving into book 2 soon this was honestly one of the best surprises of the month. The thing I like is the balance it maintains and how it's essential for both the romance and the plot because like if you go in just for the plot you'll find it very slow but if you go in just for the romance it'll feel very long so the balance between that made this book so much better.

The characters, we have Silla our main character and thank god she wasnt an obnoxious brat because that is getting way too common, she was a little naive but she also had everyone fooled lmaoo so that was very fun to read, her journey overall was so enjoyable and the transition that her character goes through with how her feelings evolve and change were the pinnacle of this book for me, I enjoyed that part so much. Jonas was one of our MMC's and eugh I didnt trust him one bit nor did I like him, he was a rat and I didnt like him + he reminded me a lot of those conservative men and bleckh like I liked him at the start and the middle but then everything just did a complete 180 and I moved on. Rey 🫦 He was THE man, I loved him so much and honestly this would be the perfect slow burn and hate to love that we might witness because like??? the tension and angst between them and the way they would be staring at each other thinking that the other doesnt know and AHHHH I loved the dynamic and banter that these two shared I loved it. He was certainly wayyy better than Jonas.

Romance was so good and so hot, I'm rooting for Silla and Rey but some of the scenes that Silla had with Jonas were so hot I cant even lie but ugh I didnt like him, he didnt think and was very impulsive and got her into trouble way too often and then there was Rey the one who was considerate and the one who actually was rooting for her and wanted her to get the thing that she wanted done, done. I loved the banter between Rey and Silla and the moments between them were so 🫦 I cant even lie. The romance itself was very well written like you'd be sucked into it and thats what I liked about it and I heard it was getting compared to ACOTAR and I dont think it's similar at all maybe the idea of it? but overall it's different.

Plot & Worldbuilding, was so entertaining to read, the plot. it was very engrossing and the things that were slowly being unraveled were so frustrating because I just wanted to know :( but I loved it and LMAOO the way Silla literally lived in denial because I lost my trust in her with the way things were being revealed left and right but it was a fun part. The only reason the book isn't a 5 is because I feel it severely lacked when it came to the world building and the magic system, there's very little of it, maybe we'll get more of it in book but we got like pinches of it considering the length of this novel, I didn't mind it that much because I enjoyed this book a lot but the absence was felt as they are an integral part of this genre.

Overall, I would recommend it.
___
Maybe a Viking romantic fantasy is all I need 🙂‍↕️

-I literally read 10 chapters in one sitting (it's like A fate inked in blood but 10x better so far!!)"""

# Chunk text without splitting sentences
chunks = chunk_text(long_text, max_tokens=500)

# Summarize each chunk
summaries = [summarizer(chunk, max_length=15, min_length=10, do_sample=False)[0]["summary_text"] for chunk in chunks]

# Combine summarized chunks
final_summary = " ".join(summaries)

print(final_summary)
