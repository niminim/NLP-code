# Speech-to-Text Demo with Whisper

A clean, Apple-style Gradio web application for speech-to-text transcription using OpenAI's Whisper Large V3 Turbo model.

## Features

- 🎤 Upload audio files (WAV, MP3, and other common formats)
- ✨ Clean, modern Apple-inspired UI with blue and white theme
- 📄 Download transcriptions as plain text (.txt)
- 📋 Download transcriptions as JSON with metadata (.json)
- ⚡ Efficient model loading (lazy initialization, cached pipeline)
- 🔄 Automatic transcription on file upload

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python app.py
```

The app will start on `http://localhost:7860` (or the port specified in the code).

## How It Works

1. **Model Backend** (`model_backend.py`):
   - Uses Hugging Face Transformers pipeline with `openai/whisper-large-v3-turbo`
   - Lazy loads the model on first use (3.6 GB model)
   - Caches the pipeline for efficient reuse

2. **I/O Utilities** (`io_utils.py`):
   - Creates temporary text and JSON files for downloads
   - Handles UTF-8 encoding properly

3. **Gradio App** (`app.py`):
   - Provides a clean, responsive web interface
   - Handles file uploads and transcription
   - Manages download file generation and visibility

## Model Information

- **Model**: `openai/whisper-large-v3-turbo`
- **Size**: 3.6 GB
- **Device**: Automatically uses GPU if available, otherwise CPU

## File Structure

```
STT_Gardio/
├── app.py              # Main Gradio application
├── model_backend.py    # Whisper model wrapper
├── io_utils.py         # File I/O utilities
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Notes

- The model will be downloaded automatically on first use (requires internet connection)
- Model loading may take a few minutes on first run
- Transcription speed depends on audio length and available hardware (GPU recommended)
- Temporary files are created for downloads and cleaned up automatically by the system
