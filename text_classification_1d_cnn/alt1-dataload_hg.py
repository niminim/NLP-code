import os
import pandas as pd
from datasets import load_dataset

# Define constants for dataset paths
data_dir = '/home/nim/venv/NLP-code/text_classification_1d_cnn/imdb_data'
train_csv_path = os.path.join(data_dir, "imdb_train.csv")
test_csv_path = os.path.join(data_dir, "imdb_test.csv")

# Create directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Load the IMDb dataset using Hugging Face's `datasets`
dataset = load_dataset('imdb')

# Convert to pandas DataFrames
train_df = pd.DataFrame(dataset['train'])
test_df = pd.DataFrame(dataset['test'])

# Save the DataFrames as CSV files
train_df.to_csv(train_csv_path, index=False)
test_df.to_csv(test_csv_path, index=False)

# Print a sample from the train and test sets
print("Sample from train set:")
print(train_df.head())
print("Sample from test set:")
print(test_df.head())