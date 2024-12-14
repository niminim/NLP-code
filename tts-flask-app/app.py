from flask import Flask, request, render_template, jsonify
from tts_model import TTSModel
import os
import uuid  # For generating unique filenames

# Initialize the Flask app
app = Flask(__name__)

# Initialize the TTS model
tts_model = TTSModel()

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        try:
            # Get the text and speaker selection from the form
            text = request.form.get('text', '').strip()
            speaker = request.form.get('speaker', 'ralph').lower()  # Default to 'ralph'

            if not text:
                return jsonify({"error": "No text provided"}), 400

            # Set the speaker_wav based on the selected speaker
            if speaker == 'ralph':
                speaker_wav_path = "/home/nim/Documents/ralph.wav"
            elif speaker == 'amanda':
                speaker_wav_path = "/home/nim/Documents/amanda_leigh2.wav"
            else:
                return jsonify({"error": "Invalid speaker selected"}), 400

            # Ensure the speaker reference file exists
            if not os.path.exists(speaker_wav_path):
                raise FileNotFoundError(f"Speaker reference file not found: {speaker_wav_path}")

            # Generate a unique file name for the audio
            unique_filename = f"static/{uuid.uuid4().hex}.wav"

            # Generate the audio file
            tts_model.generate_audio(text, output_path=unique_filename, speaker_wav=speaker_wav_path)

            # Check if the file exists
            if not os.path.exists(unique_filename):
                raise FileNotFoundError(f"Audio file not found: {unique_filename}")

            # Return the audio URL to the frontend
            return jsonify({"audio_url": f"/{unique_filename}"})

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)