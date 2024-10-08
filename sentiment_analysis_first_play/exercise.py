from transformers import pipeline

# Load the sentiment analysis pipeline using DistilBERT
nlp = pipeline("sentiment-analysis")

# Define a list of texts to analyze
texts = [
    "I love using Hugging Face transformers, they are so easy to use!",
    "I had a bad experience with the product.",
    "The weather today is beautiful."
]

# Run the sentiment analysis
results = nlp(texts)

# Display the results
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Sentiment: {result['label']}, Score: {result['score']}\n")

