
####################### Train the model
from transformers import Trainer, TrainingArguments, DistilBertForSequenceClassification, DistilBertTokenizer
from datasets import load_dataset

# Load dataset
dataset = load_dataset('imdb')

# Load model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Define training arguments with fp16 enabled
training_args = TrainingArguments(
    output_dir="/home/nim/venv/NLP-code/results",
    report_to=[],  # Disable all external reporting (Neptune, WandB, etc.) (Neptune is default)
    logging_dir="/home/nim/venv/NLP-code/logs",  # Log locally instead (if needed)
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    fp16=True,  # Enable FP16 training
)

print(training_args)


# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"]
)

# Train the model
trainer.train()

next(model.parameters()).is_cuda

# Save the model and tokenizer after training
model.save_pretrained("/home/nim/venv/NLP-code/results_manual")
tokenizer.save_pretrained("/home/nim/venv/NLP-code/results_manual")

####################### End of training


####################### Inference
import torch
import torch.nn.functional as F
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Load the model from the output directory
model = DistilBertForSequenceClassification.from_pretrained("/home/nim/venv/NLP-code/results_manual")
model = model.to(device)

# Load the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")



def predict_sentiment(text, device):
    # Tokenize the input text
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")

    # Move input tensors to the same device as the model
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Run the model in evaluation mode
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the logits
    logits = outputs.logits

    # Apply softmax to get probabilities
    probabilities = F.softmax(logits, dim=-1)

    # Get the predicted class and confidence score
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    confidence_score = torch.max(probabilities).item()

    # Map the predicted class (0 or 1) to a sentiment label
    sentiment = "Positive" if predicted_class == 1 else "Negative"

    return sentiment, confidence_score


# Example sentence
texts = [
    "I loved the movie, it was fantastic!",
    "This was the worst film I've ever seen.",
    "The plot was quite interesting, and the acting was solid.",
    "I really did not enjoy this movie, it was boring."
]

# Predict sentiment for each sentence and print with confidence score
for text in texts:
    sentiment, confidence = predict_sentiment(text, device)
    print(f"Text: {text}\nPredicted Sentiment: {sentiment}\nConfidence Score: {confidence:.4f}\n")


#### Evaluate the test-set
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')  # or 'Qt5Agg' depending on your system

# Evaluate the model on the full test set using the Trainer
results = trainer.evaluate()

# Print the evaluation results (e.g., accuracy, loss, etc.)
print("Evaluation on Full Test Set:")
print(results)
###

#### Evaluate a subset of the test-set

# Evaluate a subset of the test-set (first 10 samples in this case)
test_texts = dataset['test']['text'][:10]  # Taking first 10 examples for the subset
real_labels = dataset['test']['label'][:10]  # Get the corresponding real labels

test_texts = dataset['test']['text'][-10:]  # Taking first 10 examples for the subset
real_labels = dataset['test']['label'][-10:]  # Get the corresponding real labels


# Initialize variables for accuracy calculation
correct_predictions = 0
predicted_classes = []


# Display the results for each sample
print("Evaluation on a Subset of the Test Set with Confidence Scores:")
for text, real_label in zip(test_texts, real_labels):
    # Use the predict_sentiment function to get the predicted sentiment and confidence
    predicted_sentiment, confidence_score = predict_sentiment(text, device)

    # Map the predicted sentiment to numeric class (0 for Negative, 1 for Positive)
    predicted_class = 1 if predicted_sentiment == "Positive" else 0
    predicted_classes.append(predicted_class)

    # Check if the prediction matches the real label
    correct_predictions += 1 if predicted_class == real_label else 0

    # Display the result
    print(f"Text: {text}\nReal Sentiment: {real_label}\nPredicted Sentiment: {predicted_sentiment}\nConfidence Score: {confidence_score:.4f}\n")

# Calculate the accuracy
accuracy = correct_predictions / len(real_labels)
print(f"Accuracy on the subset: {accuracy:.2%}")

# Generate the confusion matrix
cm = confusion_matrix(real_labels, predicted_classes)

# Plot the confusion matrix using seaborn
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Negative", "Positive"], yticklabels=["Negative", "Positive"])
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()