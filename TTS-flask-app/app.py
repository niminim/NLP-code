from flask import Flask, request, jsonify, render_template
from TTS.api import TTS
from tts_model import Basic_TTSModel  # Import Basic_TTSModel for the light model
import torch
import os

app = Flask(__name__)

# Initialize Heavier TTSModel
heavier_tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda" if torch.cuda.is_available() else "cpu")


@app.route("/", methods=["GET", "POST"])
def convert_to_speech():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        data = request.get_json()
        print("DEBUG: Received POST data:", data)

        text = data.get("text")
        model = data.get("model")
        speaker = data.get("speaker", None)  # Speaker is only relevant for the heavier model
        output_file_suffix = speaker if speaker else "default"  # Use speaker or 'default'
        output_path = f"static/output_{output_file_suffix}.wav"  # Dynamic output path

        try:
            if model == "light":
                # Light model processing
                print("DEBUG: Light model selected.")
                Basic_TTSModel.generate_audio(text, output_path)
                print(f"DEBUG: Light model audio saved to {output_path}")
            elif model == "heavier":
                # Heavier model processing
                print("DEBUG: Heavier model selected.")
                speaker_wav = f"/home/nim/Documents/{speaker}.wav"
                print(f"DEBUG: Expected speaker WAV file: {speaker_wav}")

                # Check if the speaker file exists
                if not os.path.isfile(speaker_wav):
                    error_message = f"Speaker WAV file not found: {speaker_wav}"
                    print(f"DEBUG: {error_message}")
                    return jsonify({"error": error_message}), 400

                heavier_tts_model.tts_to_file(
                    text=text,
                    speaker_wav=speaker_wav,
                    language="en",
                    file_path=output_path
                )
                print(f"DEBUG: Heavier model audio saved to {output_path}")
            else:
                # Invalid model selected
                return jsonify({"error": "Invalid model selection"}), 400

            # Check if the output file was generated
            if not os.path.isfile(output_path):
                print("DEBUG: Output file not generated.")
                return jsonify({"error": "Failed to generate audio file."}), 500

            # Return success response with audio URL
            return jsonify({"message": "Conversion completed successfully", "audio_url": f"/{output_path}"})

        except Exception as e:
            print("DEBUG: Exception occurred:", e)
            return jsonify({"error": "An error occurred during conversion"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



###################################### Split, but with no semicolon
# from flask import Flask, request, jsonify, render_template, send_file
# import re
# from TTS.api import TTS
# from pydub import AudioSegment
# import os
# import torch
#
# # Import preprocessing functions
# from text_preprocessing import (
#     replace_newline_sequences,
#     process_chunk_add_new_section,
#     process_chunk_replace_quotes_newline,
#     replace_right_quote_newline,
#     process_chunk_replace_quotes_newlines,
#     replace_newline_after_quote,
# )
#
# app = Flask(__name__)
#
# # Initialize TTS models
# light_tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  # Single-speaker model
# heavier_tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(
#     "cuda" if torch.cuda.is_available() else "cpu"
# )
#
# # Function to preprocess text
# def preprocess_text(text):
#     """
#     Apply all preprocessing steps in sequence.
#     """
#     text = replace_newline_sequences(text)
#     text = process_chunk_add_new_section(text)
#     text = process_chunk_replace_quotes_newline(text)
#     text = replace_right_quote_newline(text)
#     text = process_chunk_replace_quotes_newlines(text)
#     text = replace_newline_after_quote(text)
#     return text
#
# # Function to split text into sentences
# def split_text_into_sentences(text):
#     """
#     Splits the input text into sentences based on punctuation rules.
#     """
#     text = preprocess_text(text)
#     sentences = re.split(r'(?<=[.!?])\s+', text.strip())
#     return sentences
#
# # Function to process and combine audio
# def process_and_combine_audio(
#     sentences, output_file="static/output_combined.wav", tts_model=None, speaker_wav=None
# ):
#     audio_parts = []
#
#     for i, sentence in enumerate(sentences):
#         print(f"Processing sentence {i + 1}/{len(sentences)}: {sentence}")
#         temp_output = f"temp_output_{i}.wav"
#
#         # Generate TTS for each sentence
#         tts_model.tts_to_file(
#             text=sentence,
#             speaker_wav=speaker_wav,  # Optional for speaker reference
#             language="en",
#             file_path=temp_output,
#         )
#
#         # Load the audio file into pydub
#         audio_parts.append(AudioSegment.from_file(temp_output))
#
#     # Combine all audio parts
#     combined_audio = sum(audio_parts)
#     combined_audio.export(output_file, format="wav")
#     print(f"Combined audio saved to {output_file}")
#
#     # Clean up temporary files
#     for i in range(len(sentences)):
#         os.remove(f"temp_output_{i}.wav")
#
#     return output_file
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "GET":
#         return render_template("index.html")
#
#     elif request.method == "POST":
#         try:
#             data = request.get_json()
#             text = data.get("text")
#             model = data.get("model", "light")  # Default to light model
#             speaker = data.get("speaker", None)  # Speaker is optional
#
#             if not text.strip():
#                 return jsonify({"error": "Text input is empty"}), 400
#
#             print("DEBUG: Received POST data:", data)
#             print("DEBUG: Selected model:", model)
#             print("DEBUG: Selected speaker:", speaker)
#
#             # Split text into sentences
#             sentences = split_text_into_sentences(text)
#             print("DEBUG: Sentences split:", sentences)
#
#             # Determine which model to use
#             if model == "light":
#                 # Light model does not use a speaker
#                 output_audio = process_and_combine_audio(
#                     sentences, output_file="static/output_light.wav", tts_model=light_tts
#                 )
#             elif model == "heavier":
#                 # Validate speaker file for the heavier model
#                 speaker_wav = f"/home/nim/Documents/{speaker}.wav" if speaker else None
#                 if speaker and not os.path.isfile(speaker_wav):
#                     return jsonify(
#                         {"error": f"Speaker WAV file not found: {speaker_wav}"}
#                     ), 400
#
#                 output_audio = process_and_combine_audio(
#                     sentences, tts_model=heavier_tts, speaker_wav=speaker_wav
#                 )
#
#             # Return the combined audio file URL
#             return jsonify(
#                 {"message": "Audio generated successfully", "audio_url": f"/{output_audio}"}
#             )
#
#         except Exception as e:
#             print("DEBUG: Exception occurred:", e)
#             return jsonify({"error": "An error occurred during processing"}), 500
#
#
# @app.route("/static/<path:filename>")
# def serve_static_file(filename):
#     file_path = os.path.join("static", filename)
#     if os.path.isfile(file_path):
#         return send_file(file_path, as_attachment=True)
#     return jsonify({"error": "File not found"}), 404
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)



## Hello, I'm Emilia Clarke, and I'm here to help you. How can I help?
#
# Oh, really?!? Wow!! That's impressive!

