from transformers import pipeline

gen = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B")
print(gen("Once upon a time,")[0]["generated_text"])