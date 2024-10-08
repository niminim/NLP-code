import os
import pandas as pd
import requests
import tarfile

# Define constants for dataset paths and URLs
DATA_DIR = '/home/nim/venv/NLP-code/text_classification_1d_cnn/imdb_data'
TRAIN_DIR = os.path.join(DATA_DIR, 'aclImdb', 'train')
TEST_DIR = os.path.join(DATA_DIR, 'aclImdb', 'test')
DATASET_URL = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
DATASET_TAR_PATH = os.path.join(DATA_DIR, "aclImdb_v1.tar.gz")


# Step 1: Function to create necessary directories
def create_directories():
    """
    Creates the necessary directories for storing the dataset.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Directory {DATA_DIR} created or already exists.")


# Step 2: Function to download the IMDb dataset if not already downloaded
def download_dataset():
    """
    Downloads the IMDb dataset if it is not already downloaded.
    """
    if not os.path.exists(DATASET_TAR_PATH):
        print("Downloading the IMDb dataset...")
        response = requests.get(DATASET_URL, stream=True)
        with open(DATASET_TAR_PATH, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("IMDb dataset already downloaded.")


# Step 3: Function to extract the dataset if it is not already extracted
def extract_dataset():
    """
    Extracts the IMDb dataset if the 'aclImdb' directory does not already exist.
    """
    if not os.path.exists(os.path.join(DATA_DIR, 'aclImdb')):
        print("Extracting the dataset...")
        with tarfile.open(DATASET_TAR_PATH, 'r:gz') as tar:
            tar.extractall(path=DATA_DIR)
        print("Extraction complete.")
    else:
        print("IMDb dataset already extracted.")


# Step 4: Function to load IMDb data from text files into a pandas DataFrame
def load_imdb_from_text(data_dir):
    """
    Loads reviews from the IMDb dataset (pos and neg) into a pandas DataFrame.

    Parameters:
        data_dir (str): The directory where 'pos' and 'neg' subdirectories are located.

    Returns:
        pd.DataFrame: DataFrame containing the reviews and labels.
    """
    reviews = []  # List to store the text of the reviews
    labels = []   # List to store the corresponding labels (1 for pos, 0 for neg)

    # Iterate over the two categories: 'pos' for positive reviews and 'neg' for negative reviews
    for label in ['pos', 'neg']:
        folder_path = os.path.join(data_dir, label)  # Construct the path for each category ('pos' or 'neg')

        # Ensure that the 'pos' and 'neg' directories exist; if not, create them
        os.makedirs(folder_path, exist_ok=True)

        # Iterate over all files in the current category's folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)  # Construct the full path to the review file

            # Check if the current path is a file (to avoid issues with directories)
            if os.path.isfile(file_path):
                # Open and read the review file's content
                with open(file_path, 'r', encoding='utf-8') as file:
                    reviews.append(file.read())  # Append the review text to the reviews list

                    # Append the corresponding label (1 for 'pos', 0 for 'neg') to the labels list
                    labels.append(1 if label == 'pos' else 0)

    # Return a pandas DataFrame where each review is associated with its corresponding label
    return pd.DataFrame({'review': reviews, 'label': labels})


# Step 5: Function to save a DataFrame as a CSV file
def save_dataframe_to_csv(df, output_path):
    """
    Saves a pandas DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): The DataFrame to be saved.
        output_path (str): The path where the CSV file will be saved.
    """
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")


# Step 6: Function to load the dataset, process it, and save it to CSV files
def process_and_save_imdb_dataset():
    """
    Downloads, extracts, and processes the IMDb dataset, then saves the data to CSV files.
    """
    create_directories()  # Create the necessary directories
    download_dataset()    # Download the dataset if necessary
    extract_dataset()     # Extract the dataset if not already done

    # Load the training and testing data
    print("Loading train data...")
    train_df = load_imdb_from_text(TRAIN_DIR)
    print("Loading test data...")
    test_df = load_imdb_from_text(TEST_DIR)

    # Save the datasets to CSV files
    train_csv_path = os.path.join(DATA_DIR, "imdb_train.csv")
    test_csv_path = os.path.join(DATA_DIR, "imdb_test.csv")
    save_dataframe_to_csv(train_df, train_csv_path)
    save_dataframe_to_csv(test_df, test_csv_path)

    # Print a sample from the saved CSVs
    print("Sample from train set:")
    print(train_df.head())
    print("Sample from test set:")
    print(test_df.head())


# Main execution flow
if __name__ == "__main__":
    process_and_save_imdb_dataset()