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
dataset = load_dataset('imdb')


# Step 2: Preprocess the data (tokenization and padding)
# We'll use a simple space-based tokenizer for this exercise
def tokenize(text):
    return text.split()


# Build a vocabulary from the dataset
def build_vocab(sentences, vocab_size=10000):
    word_count = {}
    for sentence in sentences:
        for word in tokenize(sentence):
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1
    sorted_vocab = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:vocab_size]
    vocab = {word: idx + 2 for idx, (word, _) in enumerate(sorted_vocab)}  # 0 for padding, 1 for unknown
    vocab['<PAD>'] = 0
    vocab['<UNK>'] = 1
    return vocab


# Convert text to sequence of token indices
def text_to_sequence(text, vocab, max_len=256):
    tokenized = tokenize(text)
    sequence = [vocab.get(word, vocab['<UNK>']) for word in tokenized]
    if len(sequence) > max_len:
        sequence = sequence[:max_len]
    else:
        sequence += [vocab['<PAD>']] * (max_len - len(sequence))  # Padding
    return sequence


# Build the vocabulary from the train set
train_texts = [example['text'] for example in dataset['train']]
vocab = build_vocab(train_texts)

# Apply text_to_sequence to the train and test datasets
X_train = [text_to_sequence(example['text'], vocab) for example in dataset['train']]
y_train = [example['label'] for example in dataset['train']]
X_test = [text_to_sequence(example['text'], vocab) for example in dataset['test']]
y_test = [example['label'] for example in dataset['test']]

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train)
y_train_tensor = torch.tensor(y_train)
X_test_tensor = torch.tensor(X_test)
y_test_tensor = torch.tensor(y_test)

# Step 3: Create a PyTorch dataset and dataloader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

batch_size = 64  # Batch size for training
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


# Step 4: Define the CNN model for text classification
class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_size, num_classes=2):
        super(TextCNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=0)  # Embedding layer
        self.conv1 = nn.Conv1d(in_channels=embed_size, out_channels=128, kernel_size=5)  # Conv1d layer
        self.pool = nn.AdaptiveMaxPool1d(1)  # Max pooling
        self.fc = nn.Linear(128, num_classes)  # Fully connected layer

    def forward(self, x):
        embedded = self.embedding(x).permute(0, 2, 1)  # Reshape for Conv1d (batch_size, embed_size, sequence_length)
        conv_out = F.relu(self.conv1(embedded))
        pooled = self.pool(conv_out).squeeze(2)
        out = self.fc(pooled)
        return out


# Initialize the model
vocab_size = len(vocab)
embed_size = 100  # Embedding size
model = TextCNN(vocab_size=vocab_size, embed_size=embed_size)

# Step 5: Define loss and optimizer
criterion = nn.CrossEntropyLoss()  # Cross entropy loss for classification
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer


# Step 6: Train the model
def train_model(model, train_loader, criterion, optimizer, num_epochs=5):
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
            preds = outputs.argmax(dim=1)
            correct += (preds == targets).sum().item()

        accuracy = correct / len(train_loader.dataset)
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss / len(train_loader)}, Accuracy: {accuracy:.4f}')


# Train the model for 5 epochs
train_model(model, train_loader, criterion, optimizer, num_epochs=5)


# Step 7: Evaluate the model
def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for inputs, targets in test_loader:
            outputs = model(inputs)
            preds = outputs.argmax(dim=1)
            correct += (preds == targets).sum().item()

    accuracy = correct / len(test_loader.dataset)
    print(f'Test Accuracy: {accuracy:.4f}')


# Evaluate the model on the test set
evaluate_model(model, test_loader)