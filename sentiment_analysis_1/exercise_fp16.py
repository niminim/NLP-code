### Enable FP16 Precision for Inference
# To use FP16 precision for inference, you can use the pipeline method and enable FP16 by specifying the device (if a GPU is available)
# and enabling half precision.

# Here's how to modify the sentiment analysis example:

from transformers import pipeline
import torch

# Check if a GPU is available
device = 0 if torch.cuda.is_available() else -1

# Load the DistilBERT sentiment analysis pipeline with FP16 precision on the right device
nlp = pipeline("sentiment-analysis", model="distilbert-base-uncased", device=device)

# Test sentences
texts = [
    "I love using Hugging Face transformers, they are so easy to use!",
    "I had a bad experience with the product.",
    "The weather today is beautiful."
]

# Run sentiment analysis (note: no 'device' argument needed here)
results = nlp(texts)

# Display the results
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Sentiment: {result['label']}, Score: {result['score']}\n")