from flask import Flask, request, send_file, jsonify
import os
from tts_model import TTSModel  # Import the TTS model class

app = Flask(__name__)

# Initialize the TTS model
tts_model = TTSModel()

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    """
    Endpoint to convert text to speech and return an audio file.
    """
    try:
        # Get the text from the POST request
        data = request.json
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Generate the audio file
        audio_path = "output.wav"  # Temporary output file
        tts_model.generate_audio(text, output_path=audio_path)

        # Return the audio file
        return send_file(audio_path, mimetype='audio/wav', as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)