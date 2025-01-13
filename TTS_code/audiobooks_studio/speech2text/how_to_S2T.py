# Pipeline:
# The following is done automatically:
#
# Loads the model (WhisperForConditionalGeneration) and processor (WhisperProcessor).
# Preprocesses audio (e.g., resampling, normalization).
# Runs the model for inference.
# Decodes the model’s output into human-readable text.


from transformers import pipeline

file_path = "/home/nim/Baroness_of_Blood2_by_ralph_lister_350/audio/One/part2.wav"

whisper_type = 'large-v3-turbo' # base - 0.55 GB,  small - 1.4 GB, medium - 3.5 GB, large - 7GB, large-V2 - 7GB,  large-V3 - 7GB
# large-v3-turbo - 3.6 GB
stt_pipeline = pipeline("automatic-speech-recognition", model=f"openai/whisper-{whisper_type}")

result = stt_pipeline(file_path)
print(result["text"])
###



# to show all models
from huggingface_hub import list_models

# Increase limit to retrieve more models
models = list_models(filter="task:automatic-speech-recognition", limit=100)

# Print the model IDs
for model in models:
    print(model.modelId)


############################

# Manual Use:
# You need to perform each step explicitly:
#
# Load the processor and model.
# Process the input audio into model-compatible format.
# Run inference on the processed audio.
# Decode the raw model output into readable text.


from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf

# Load model and processor
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
processor = WhisperProcessor.from_pretrained("openai/whisper-small")

# Load and preprocess audio
audio_input, sample_rate = sf.read(file_path)
input_features = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_features

# Generate transcription
generated_ids = model.generate(input_features)
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(transcription)
############################


# Performance and Efficiency
# Pipeline: Suitable for standard use cases. The convenience may add slight overhead, as it assumes defaults for preprocessing and decoding.
# Processor + Model: You can optimize for specific use cases (e.g., change decoding strategies like beam search, fine-tune parameters)
# and potentially achieve better performance.

# Decoding Strategies
# Pipeline: Uses a default decoding strategy.
# Processor + Model: You can control the decoding strategy (e.g., greedy, beam search, temperature) by passing arguments to model.generate.

# Your Implementation: (from Speech2text)
# Custom code to process multiple audio files in a directory.
# Integrates preprocessing, model inference, and file output management.
# Designed for batch processing in a production-like pipeline.


# pip install huggingface_hub[cli]
# huggingface-cli scan-cache
# huggingface - cli delete - cache
# access cache: cd /home/nim/.cache/huggingface/hub
