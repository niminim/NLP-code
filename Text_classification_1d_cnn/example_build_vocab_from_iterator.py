from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# Sample text data
text_data = [
    "I love machine learning",
    "Deep learning is amazing",
    "I enjoy coding in Python"
]

# Define a tokenizer
tokenizer = get_tokenizer("basic_english")

# Function to yield tokens (words) from text
def yield_tokens(data_iter):
    for text in data_iter:
        yield tokenizer(text)

# Build vocabulary from the tokenized text data
vocab = build_vocab_from_iterator(yield_tokens(text_data), specials=["<unk>", "<pad>"])
vocab.set_default_index(vocab["<unk>"])  # Handle unknown words

# Let's see the vocabulary
print(vocab.get_stoi())  # String-to-index mapping (word -> index)