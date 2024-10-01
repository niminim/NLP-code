
# 1. Load or Prepare Text Data
import gensim
from gensim.models import Word2Vec
from nltk.corpus import brown
import nltk

# Downloading dataset
nltk.download('brown')

# Load a sample corpus from the NLTK library
sentences = brown.sents()

# 2. Train the Word2Vec Model
# Training Word2Vec model
model = Word2Vec(sentences, vector_size=100, window=5, min_count=5, sg=1)

# Save the model for later use
model.save("word2vec.model")

# 3. Loading a Pretrained Model
import gensim.downloader as api

# Download the pretrained Word2Vec model (Google's trained model)
pretrained_model = api.load('word2vec-google-news-300')

# Or load from a file if you have it
# pretrained_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)


# 4. Use Cases of Word2Vec

# 4.1 Finding Word Similarity
# Find words similar to 'king'
similar_words = model.wv.most_similar('king', topn=5)
print(similar_words)

# With the pretrained model
pretrained_similar_words = pretrained_model.most_similar('king', topn=5)
print(pretrained_similar_words)

# 4.2 Word Analogies
# Word analogy example: "king - man + woman = ?"
result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
print(result)

# With the pretrained model
pretrained_result = pretrained_model.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
print(pretrained_result)

# 4.3 Finding Odd-One-Out
# Find the word that doesn't match the others
odd_word = model.wv.doesnt_match(['breakfast', 'lunch', 'dinner', 'king'])
print(odd_word)

# With the pretrained model
pretrained_odd_word = pretrained_model.doesnt_match(['breakfast', 'lunch', 'dinner', 'king'])
print(pretrained_odd_word)


# 4.4 Visualizing Word Embeddings
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # or 'Qt5Agg' depending on your system

# Reduce dimensions using TSNE
words = list(model.wv.key_to_index)[:100]  # First 100 words
word_vectors = np.array([model.wv[word] for word in words])  # Convert to NumPy array

tsne = TSNE(n_components=2)
reduced_vectors = tsne.fit_transform(word_vectors)

# Plotting
plt.figure(figsize=(10, 10))
for i, word in enumerate(words):
    plt.scatter(reduced_vectors[i][0], reduced_vectors[i][1])
    plt.annotate(word, xy=(reduced_vectors[i][0], reduced_vectors[i][1]))

# Save the plot as an image (e.g., PNG)
plt.savefig('/home/nim/venv/NLP-code/gensim_word2vec/word2vec_visualization.png')
plt.show()


# 4.5 Document Similarity
# Get vector for a specific word
word_vector = model.wv['king']

# Compute similarity between two words
similarity = model.wv.similarity('king', 'queen')
print(similarity)

# With pretrained model
pretrained_similarity = pretrained_model.similarity('king', 'queen')
print(pretrained_similarity)

# 5. Fine-Tuning the Word2Vec Model
new_sentences = [['new', 'data', 'to', 'train']]

# Continue training the model with new sentences
model.build_vocab(new_sentences, update=True)
model.train(new_sentences, total_examples=len(new_sentences), epochs=model.epochs)