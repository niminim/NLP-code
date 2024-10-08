import os
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from datasets import load_dataset
from torch.nn.utils.rnn import pad_sequence
import torch.nn.functional as F

# Step 1: Load the IMDb dataset using Hugging Face's datasets library
print("Loading IMDb dataset...")
dataset = load_dataset('imdb')  # Automatically downloads and loads the IMDb dataset

# Step 2: Preprocess the data (tokenization and padding)

# Tokenize the text by splitting on spaces
# Tokenization is the process of converting a sentence into individual words or tokens.
def tokenize(text):
    return text.split()

# Build a vocabulary from the dataset
# This function creates a word-to-index mapping (vocabulary) and limits the vocabulary size to 10,000.
def build_vocab(sentences, vocab_size=10000):
    word_count = {}  # Dictionary to store word frequencies
    for sentence in sentences:
        for word in tokenize(sentence):  # Split each sentence into words
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1
    # Sort the vocabulary by frequency and keep only the top `vocab_size` words
    sorted_vocab = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:vocab_size]
    # Assign an index to each word, starting from 2 (0 is for padding, 1 is for unknown words)
    vocab = {word: idx + 2 for idx, (word, _) in enumerate(sorted_vocab)}
    vocab['<PAD>'] = 0  # Padding token
    vocab['<UNK>'] = 1  # Unknown token
    return vocab

# Convert text to sequence of token indices
# This function maps each word in the sentence to its corresponding index in the vocabulary.
# It also handles padding to ensure all sequences have the same length.
def text_to_sequence(text, vocab, max_len=256):
    tokenized = tokenize(text)  # Split the text into tokens
    sequence = [vocab.get(word, vocab['<UNK>']) for word in tokenized]  # Map each word to its index
    if len(sequence) > max_len:
        sequence = sequence[:max_len]  # Truncate the sequence if it's too long
    else:
        sequence += [vocab['<PAD>']] * (max_len - len(sequence))  # Pad the sequence if it's too short
    return sequence

# Build the vocabulary from the training set
train_texts = [example['text'] for example in dataset['train']]  # Extract texts from the training set
vocab = build_vocab(train_texts)  # Build the vocabulary using the training texts

# Apply text_to_sequence to the train and test datasets
# Convert the texts in both the training and test sets to sequences of word indices
X_train = [text_to_sequence(example['text'], vocab) for example in dataset['train']]
y_train = [example['label'] for example in dataset['train']]
X_test = [text_to_sequence(example['text'], vocab) for example in dataset['test']]
y_test = [example['label'] for example in dataset['test']]

# Convert data to PyTorch tensors
# This step is necessary for working with PyTorch models
X_train_tensor = torch.tensor(X_train)
y_train_tensor = torch.tensor(y_train)
X_test_tensor = torch.tensor(X_test)
y_test_tensor = torch.tensor(y_test)

# Step 3: Create a PyTorch dataset and dataloader
# The dataset is a container for our data, and the dataloader helps batch the data during training/testing.
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

batch_size = 64  # Batch size for training
# DataLoader creates batches of data and allows us to shuffle the data during training
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Step 4: Define the CNN model for text classification

# This class defines the architecture of the convolutional neural network (CNN).
class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_size, num_classes=2):
        super(TextCNN, self).__init__()
        # Embedding layer: Maps word indices to dense vectors
        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=0)
        # 1D Convolutional layer: Detects local features in word sequences
        self.conv1 = nn.Conv1d(in_channels=embed_size, out_channels=128, kernel_size=5)
        # Max pooling layer: Reduces the size of the output and keeps important features
        self.pool = nn.AdaptiveMaxPool1d(1)
        # Fully connected layer: Maps the extracted features to output classes (positive/negative)
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        # Embedding layer: Converts input word indices to dense vectors
        embedded = self.embedding(x).permute(0, 2, 1)  # Permute to match input shape for Conv1d
        conv_out = F.relu(self.conv1(embedded))  # Apply convolution and ReLU activation
        pooled = self.pool(conv_out).squeeze(2)  # Max pooling to reduce the size
        out = self.fc(pooled)  # Fully connected layer for classification
        return out

# Initialize the model
vocab_size = len(vocab)  # The size of the vocabulary
embed_size = 100  # The dimension of the word embeddings
model = TextCNN(vocab_size=vocab_size, embed_size=embed_size)

# Step 5: Define loss and optimizer
# CrossEntropyLoss is commonly used for classification tasks
criterion = nn.CrossEntropyLoss()  # Loss function for multi-class classification
# Adam is a commonly used optimizer that adapts the learning rate during training
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Step 6: Train the model
# This function defines the training process for the model
def train_model(model, train_loader, criterion, optimizer, num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        correct = 0
        for batch_idx, (inputs, targets) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            preds = outputs.argmax(dim=1)  # Get the predicted class
            correct += (preds == targets).sum().item()  # Count correct predictions

        accuracy = correct / len(train_loader.dataset)  # Calculate accuracy
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss / len(train_loader)}, Accuracy: {accuracy:.4f}')

# Train the model for 5 epochs
train_model(model, train_loader, criterion, optimizer, num_epochs=5)

# Step 7: Evaluate the model
# This function defines the evaluation process for the model
def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    with torch.no_grad():  # Disable gradient calculations for evaluation
        for inputs, targets in test_loader:
            outputs = model(inputs)
            preds = outputs.argmax(dim=1)  # Get the predicted class
            correct += (preds == targets).sum().item()

    accuracy = correct / len(test_loader.dataset)
    print(f'Test Accuracy: {accuracy:.4f}')

# Evaluate the model on the test set
evaluate_model(model, test_loader)


# Evaluate the model on the test set
evaluate_model(model, test_loader)


# Explanation:
# Step 1: Load IMDb Dataset:
#
# Using Hugging Face’s datasets.load_dataset() to load the IMDb dataset, which is split into training and testing sets.
# Step 2: Preprocess the Data:
#
# Tokenization: Splits the text into words.
# Vocabulary Building: We count the most frequent words and create a mapping from words to indices.
# Text to Sequence: Each review is converted into a sequence of integers based on the vocabulary.
# Padding: All reviews are padded to the same length (max_len=256).
# Step 3: Create Datasets and Dataloaders:
#
# Convert the processed data into PyTorch tensors and load them into DataLoader objects for batching and shuffling.
# Step 4: Define CNN Model:
#
# A simple CNN model with an embedding layer, 1D convolutional layer, and a fully connected layer for binary classification (positive or negative sentiment).
# Step 5: Loss and Optimizer:
#
# Cross-Entropy Loss for classification.
# Adam Optimizer for optimizing the model weights.
# Step 6: Train the Model:
#
# Training is done for 5 epochs. During each epoch, the model’s output is calculated, loss is backpropagated, and weights are updated using the optimizer.
# Accuracy and loss are displayed for each epoch.
# Step 7: Evaluate the Model:
#
# The model’s performance is evaluated on the test set. Accuracy is calculated and printed.