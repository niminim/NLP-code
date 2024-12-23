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
