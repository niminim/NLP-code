"""
Gradio web application for speech-to-text transcription.

This app provides a clean, Apple-style interface for uploading audio files
and downloading transcriptions in both .txt and .json formats.
"""

import logging
import os
import warnings
import time
import socket
from typing import Tuple, Optional
import gradio as gr

# Suppress transformers deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", message=".*past_key_values.*")
warnings.filterwarnings("ignore", message=".*inputs.*deprecated.*")

# Set up logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mutagen import File as MutagenFile
    from mutagen.mp3 import MP3
    from mutagen.wave import WAVE
    from mutagen.flac import FLAC
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    logger.warning("mutagen not available, audio duration detection may be limited")

from model_backend import transcribe_audio
from io_utils import make_txt_file

# Apple-style CSS for clean, modern UI
CUSTOM_CSS = """
/* Apple-style design with blue and white theme */
:root {
    --primary-blue: #007AFF;
    --light-blue: #5AC8FA;
    --white: #FFFFFF;
    --light-gray: #F5F5F7;
    --border-gray: #D2D2D7;
    --text-dark: #1D1D1F;
    --text-light: #86868B;
}

/* Main container styling */
.main-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--white);
}

/* Title styling */
h1 {
    font-size: 36px;
    font-weight: 600;
    color: var(--primary-blue);
    text-align: left;
    margin-bottom: 4px;
    margin-top: 20px;
    letter-spacing: -0.5px;
}

/* Subtitle styling - elegant and light */
h2, h3 {
    font-size: 15px;
    font-weight: 300;
    color: var(--light-blue);
    text-align: left;
    margin-bottom: 30px;
    margin-top: 0px;
    font-style: normal;
    letter-spacing: 0.5px;
    line-height: 1.4;
}

/* Button styling */
.primary-button {
    background: var(--primary-blue);
    color: var(--white);
    border: none;
    border-radius: 12px;
    padding: 14px 28px;
    font-size: 17px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
}

.primary-button:hover {
    background: #0051D5;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.primary-button:active {
    transform: translateY(0);
}

/* Text area styling */
textarea {
    border-radius: 12px;
    border: 1px solid var(--border-gray);
    padding: 16px;
    font-size: 17px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--light-gray);
    color: var(--text-dark);
    resize: vertical;
    min-height: 150px;
}

textarea:focus {
    outline: none;
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

/* Audio component styling */
.audio-component {
    border-radius: 12px;
    border: 2px dashed var(--border-gray);
    padding: 40px;
    text-align: center;
    background: var(--light-gray);
    transition: all 0.2s ease;
}

.audio-component:hover {
    border-color: var(--primary-blue);
    background: rgba(0, 122, 255, 0.05);
}

/* Download button styling */
.download-button {
    background: var(--white);
    color: var(--primary-blue);
    border: 1.5px solid var(--primary-blue);
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.download-button:hover {
    background: rgba(0, 122, 255, 0.1);
}

/* Card-like containers */
.card {
    background: var(--white);
    border-radius: 16px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--border-gray);
}

/* Spacing utilities */
.spacing-large {
    margin: 32px 0;
}

.spacing-medium {
    margin: 20px 0;
}

/* Status indicator styling */
#status-indicator {
    padding: 12px 20px;
    border-radius: 10px;
    margin: 10px 0;
    font-size: 15px;
    font-weight: 500;
    background: rgba(0, 122, 255, 0.1);
    border-left: 4px solid var(--primary-blue);
    color: var(--text-dark);
}

/* Progress indicator styling */
.progress-bar {
    background: var(--primary-blue);
    border-radius: 4px;
}

/* Audio player styling */
.audio-player-container {
    margin: 15px 0;
}

.audio-player-container audio,
.audio-player-container [data-testid="audio"] {
    width: 100%;
    height: 54px;
    margin: 0;
}

/* Style the file upload area */
.audio-component {
    min-height: 80px;
    padding: 20px;
}

/* Responsive design */
@media (max-width: 768px) {
    h1 {
        font-size: 36px;
    }
    
    h2 {
        font-size: 18px;
    }
    
    .main-container {
        padding: 20px 16px;
    }
}
"""


def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file in seconds efficiently.
    Uses metadata when available to avoid loading the entire file.
    
    Args:
        audio_path: Path to the audio file.
        
    Returns:
        Duration in seconds, or 0.0 if unable to determine.
    """
    # Try mutagen first (fast - reads metadata only)
    if MUTAGEN_AVAILABLE:
        try:
            audio_file = MutagenFile(audio_path)
            if audio_file is not None and hasattr(audio_file, 'info'):
                duration = audio_file.info.length
                if duration and duration > 0:
                    return duration
        except Exception:
            pass  # Fall through to torchaudio
    
    # Fallback: use torchaudio (slower - loads audio data)
    try:
        import torchaudio
        # Use backend that's faster for duration only
        info = torchaudio.info(audio_path)
        if hasattr(info, 'num_frames') and hasattr(info, 'sample_rate'):
            duration = info.num_frames / info.sample_rate
            return duration
        # If info doesn't have frames, load minimal data
        waveform, sample_rate = torchaudio.load(audio_path, num_frames=1)
        # Get full duration from file size estimation or load minimal
        # Actually, let's just return 0 if we can't get it from metadata
        return 0.0
    except Exception:
        return 0.0


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to HH:MM:SS format.
    
    Args:
        seconds: Duration in seconds.
        
    Returns:
        Formatted string like "00:00:00".
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def transcribe_and_prepare_downloads(
    audio_file: Optional[str]
) -> Tuple[str, Optional[str], str]:
    """
    Transcribe audio file and prepare downloadable file.
    
    Args:
        audio_file: Path to the uploaded audio file (from Gradio File component).
                   Can be a string path or a FileData object.
        
    Returns:
        Tuple of (transcription_text_with_download_link, txt_file_path, status_message).
        Returns empty strings and None values if no file is provided or if an error occurs.
    """
    if audio_file is None:
        return "", None, ""
    
    # Handle Gradio File component input
    # File component returns a string path or FileData object
    actual_audio_path = audio_file
    
    # Extract path from FileData object or string
    if hasattr(audio_file, 'name'):
        actual_audio_path = audio_file.name
    elif isinstance(audio_file, str):
        actual_audio_path = audio_file
    elif isinstance(audio_file, tuple):
        # Extract path from tuple if needed
        actual_audio_path = audio_file[0] if len(audio_file) > 0 else None
    
    # Validate path quickly
    if not actual_audio_path:
        return "Invalid audio file format.", None, ""
    
    if not os.path.exists(actual_audio_path):
        return "Audio file not found. Please upload a valid audio file.", None, ""
    
    try:
        # Start timing the transcription immediately
        start_time = time.time()
        
        # Get audio duration efficiently (only metadata, no full file load)
        audio_duration = get_audio_duration(actual_audio_path)
        duration_str = format_duration(audio_duration) if audio_duration > 0 else "unknown"
        
        # Transcribe the audio (this is non-blocking for playback)
        # Note: Progress tracking is handled by Gradio automatically
        result = transcribe_audio(actual_audio_path)
        
        # Calculate transcription time
        transcription_time = time.time() - start_time
        
        transcription_text = result.get("text", "")
        
        if not transcription_text:
            return "No transcription generated. Please check your audio file.", None, "⚠️ **Warning:** No transcription generated."
        
        # Prepare download file
        txt_file_path = make_txt_file(transcription_text)
        
        logger.info(f"Transcription completed. File prepared: {txt_file_path}")
        
        # Get file size
        file_size = 0
        file_size_str = ""
        if txt_file_path and os.path.exists(txt_file_path):
            file_size = os.path.getsize(txt_file_path)
            if file_size < 1024:
                file_size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                file_size_str = f"{file_size / 1024:.2f} KB"
            else:
                file_size_str = f"{file_size / (1024 * 1024):.2f} MB"
        
        # Format transcription text with clickable filename and file size BELOW the text
        import urllib.parse
        if txt_file_path:
            filename = os.path.basename(txt_file_path)
            # Properly escape the file path for Gradio's file serving
            escaped_path = urllib.parse.quote(txt_file_path.replace(os.sep, '/'), safe='')
            # Create clickable filename with file size BELOW transcription
            # Use proper Gradio file URL - files are served at /file=path
            download_link_html = f'''<div style="margin-top: 12px; padding: 10px; background: #F5F5F7; border-radius: 8px; border: 1px solid #D2D2D7; display: flex; justify-content: space-between; align-items: center;">
                <a href="/file={escaped_path}" download="{filename}" style="color: #007AFF; text-decoration: none; font-weight: 500; font-size: 14px; cursor: pointer;">{filename}</a>
                <span style="color: #86868B; font-size: 12px;">{file_size_str}</span>
            </div>'''
            # Format transcription with clickable filename BELOW text
            transcription_with_link = f"<div style='white-space: pre-wrap; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif; color: #1D1D1F;'>{transcription_text}</div>{download_link_html}"
        else:
            transcription_with_link = f"<div style='white-space: pre-wrap; font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif; color: #1D1D1F;'>{transcription_text}</div>"
        
        # Format status message with duration and transcription time (file size moved to transcription area)
        status_msg = f"✅ **Transcribed {duration_str} audio file in {transcription_time:.2f} seconds**"
        if result.get("language"):
            status_msg += f" (Detected language: {result.get('language')})"
        
        return transcription_with_link, txt_file_path, status_msg
        
    except FileNotFoundError as e:
        error_msg = f"Audio file not found: {str(e)}"
        logger.error(error_msg)
        return error_msg, None, "❌ **Error:** " + error_msg
    except ValueError as e:
        error_msg = f"Invalid audio file: {str(e)}"
        logger.error(error_msg)
        return error_msg, None, "❌ **Error:** " + error_msg
    except Exception as e:
        error_msg = f"Transcription failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg, None, "❌ **Error:** " + error_msg


def create_interface():
    """Create and configure the Gradio interface."""
    
    with gr.Blocks(
        title="Speech to Text - Whisper Transcription"
    ) as demo:
        
        # Header
        gr.Markdown(
            """
            # Speech to Text Studio
            ### Powered by Whisper Large V3 Turbo
            """,
            elem_classes=["main-container"]
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # Tab interface for upload vs record
                with gr.Tabs():
                    with gr.Tab("📁 Upload File"):
                        # File upload component - instant upload, NO waveform processing
                        file_input = gr.File(
                            label="Upload Audio File",
                            file_types=[".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma", ".aac"],
                            elem_classes=["audio-component"]
                        )
                    
                    with gr.Tab("🎤 Record from Mic"):
                        # Microphone recording component
                        mic_recording = gr.Audio(
                            label="Record Audio",
                            sources=["microphone"],
                            type="filepath",
                            elem_classes=["audio-component"]
                        )
                        gr.Markdown(
                            "<div style='text-align: center; color: #86868B; font-size: 14px; margin-top: 10px;'>Click the microphone icon to start recording. Click stop when finished.</div>"
                        )
                
                # Audio player as OUTPUT - appears after upload/recording, NO waveform generation
                audio_player_output = gr.Audio(
                    label="Audio Player",
                    type="filepath",
                    visible=False,
                    elem_classes=["audio-player-container"]
                )
                
                # Status indicator for transcription progress
                status_indicator = gr.Markdown(
                    value="",
                    visible=False,
                    elem_id="status-indicator"
                )
                
                # Transcribe button
                transcribe_btn = gr.Button(
                    "🎙️ Transcribe",
                    variant="primary",
                    elem_classes=["primary-button"],
                    scale=1
                )
        
        # Transcription output (HTML to support clickable filename)
        transcription_output = gr.HTML(
            label="Transcription",
            value="<div style='padding: 15px; color: #86868B;'>Your transcription will appear here...</div>"
        )
        
        # Download section - file component for download functionality
        txt_download = gr.File(
            label="Download Transcription",
            visible=False
        )
        
        # Handle file upload - update Audio OUTPUT component (NO waveform generation)
        def handle_file_upload(file_data):
            """Update Audio OUTPUT component when file is uploaded - NO waveform processing."""
            if file_data is None:
                return gr.update(visible=False)
            
            # Extract file path
            if hasattr(file_data, 'name'):
                file_path = file_data.name
            elif isinstance(file_data, str):
                file_path = file_data
            else:
                file_path = str(file_data) if file_data else None
            
            if file_path and os.path.exists(file_path):
                # Pass path to Audio OUTPUT component - NO waveform generation
                return gr.update(value=file_path, visible=True)
            else:
                return gr.update(visible=False)
        
        # Handle microphone recording - Gradio saves it as a file automatically
        def handle_mic_recording(audio_data):
            """Handle microphone recording - audio_data is file path from Gradio.
            When recording, clears any previously uploaded file."""
            if audio_data is None:
                # Clear the player when mic recording is cleared
                return gr.update(visible=False), None
            
            # Gradio Audio component with microphone returns file path directly
            if isinstance(audio_data, tuple):
                # If tuple, extract path (first element)
                file_path = audio_data[0] if len(audio_data) > 0 else None
            elif isinstance(audio_data, str):
                file_path = audio_data
            else:
                file_path = str(audio_data) if audio_data else None
            
            if file_path and os.path.exists(file_path):
                # Update Audio OUTPUT component with new recording (replaces any uploaded file)
                # Also update file_input to use the recording for transcription (this clears old uploaded file)
                return gr.update(value=file_path, visible=True), file_path
            else:
                # Clear both when recording is cleared
                return gr.update(visible=False), None
        
        # Wire up file upload to show Audio OUTPUT component
        # But hide uploaded file if mic recording is active (to avoid showing uploaded file when recording)
        def handle_file_upload_with_mic_check(file_data, mic_data):
            """Handle file upload, but hide if mic recording is active and file doesn't match mic recording."""
            # If mic recording exists and file_data doesn't match it, hide uploaded file
            if mic_data is not None and file_data is not None:
                # Check if file_data matches mic_recording (same file)
                mic_path = None
                if isinstance(mic_data, tuple):
                    mic_path = mic_data[0] if len(mic_data) > 0 else None
                elif isinstance(mic_data, str):
                    mic_path = mic_data
                
                file_path = None
                if hasattr(file_data, 'name'):
                    file_path = file_data.name
                elif isinstance(file_data, str):
                    file_path = file_data
                
                # If file paths don't match, it's an uploaded file while mic is active - hide it
                if mic_path and file_path and mic_path != file_path:
                    return gr.update(visible=False)
            
            # Otherwise, show the file normally (either no mic active, or file matches mic recording)
            return handle_file_upload(file_data)
        
        file_input.change(
            fn=handle_file_upload_with_mic_check,
            inputs=[file_input, mic_recording],
            outputs=[audio_player_output]
        )
        
        # Wire up microphone recording - updates both audio player and file_input
        # When mic recording happens, it replaces any uploaded file
        mic_recording.change(
            fn=handle_mic_recording,
            inputs=[mic_recording],
            outputs=[audio_player_output, file_input]
        )
        
        # Wire up the callback with visibility control and progress
        def update_outputs(file_data):
            """Wrapper to handle visibility of download buttons and show progress."""
            # Extract file path
            if file_data is None:
                return "<div style='padding: 15px; color: #1D1D1F;'>Please upload an audio file first.</div>", None, ""
            
            if hasattr(file_data, 'name'):
                audio_path = file_data.name
            elif isinstance(file_data, str):
                audio_path = file_data
            else:
                audio_path = str(file_data) if file_data else None
            
            if not audio_path:
                return "<div style='padding: 15px; color: #1D1D1F;'>Please upload an audio file first.</div>", None, ""
            
            # Progress is automatically injected by Gradio
            text_html, txt_path, status_msg = transcribe_and_prepare_downloads(audio_path)
            
            # Format transcription HTML properly
            if txt_path:
                transcription_html = f"<div style='padding: 15px;'>{text_html}</div>"
            else:
                transcription_html = f"<div style='padding: 15px; color: #1D1D1F;'>{text_html}</div>"
            
            # Update file component - keep visible so user can download via Gradio's file component
            # This ensures download works reliably
            txt_update = gr.update(value=txt_path, visible=(txt_path is not None)) if txt_path else gr.update(visible=False)
            
            # Update status indicator
            status_update = gr.update(value=status_msg, visible=bool(status_msg)) if status_msg else gr.update(visible=False)
            
            return transcription_html, txt_update, status_update
        
        transcribe_btn.click(
            fn=update_outputs,
            inputs=[file_input],
            outputs=[transcription_output, txt_download, status_indicator],
            show_progress="full"
        )
        
        # Footer
        gr.Markdown(
            """
            ---
            <div style="text-align: center; color: #86868B; font-size: 14px; margin-top: 40px;">
            Upload an audio file to get started. Supports common audio formats (WAV, MP3, etc.)
            </div>
            """,
            elem_classes=["spacing-large"]
        )
    
    return demo


if __name__ == "__main__":
    import socket
    
    def find_free_port(start_port=7860, max_attempts=10):
        """Find a free port starting from start_port."""
        for i in range(max_attempts):
            port = start_port + i
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    return port
                except OSError:
                    continue
        return None  # No free port found
    
    demo = create_interface()
    
    # Try to find an available port
    port = find_free_port(7860)
    if port is None:
        logger.warning("Could not find free port, letting Gradio choose automatically")
        port = None
    
    if port and port != 7860:
        logger.info(f"Port 7860 is in use, using port {port} instead")
    
    # Get local IP address for network access
    def get_local_ip():
        """Get the local IP address for network access."""
        try:
            # Connect to a remote address to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't actually connect, just determines the local IP
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            try:
                # Fallback: get hostname IP
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                return local_ip
            except Exception:
                return None
    
    local_ip = get_local_ip()
    actual_port = port if port else 7860
    
    launch_kwargs = {
        "server_name": "0.0.0.0",  # Listen on all interfaces for network access
        "share": True,  # Enable public sharing - creates a shareable link
        "theme": gr.themes.Soft(primary_hue="blue"),
        "css": CUSTOM_CSS,
        "inbrowser": False  # Don't automatically open browser - prevents connection errors
    }
    
    if port:
        launch_kwargs["server_port"] = port
    
    # Print network access information
    print("\n" + "="*60)
    print("🚀 Gradio App Starting...")
    print("="*60)
    if local_ip:
        print(f"\n📱 To access from your phone on the same network:")
        print(f"   http://{local_ip}:{actual_port}")
        print(f"\n💻 Local access:")
        print(f"   http://localhost:{actual_port}")
    else:
        print(f"\n💻 Local access:")
        print(f"   http://localhost:{actual_port}")
        print(f"\n⚠️  Could not detect local IP. Use 'ip addr' or 'ifconfig' to find your IP.")
    print("="*60 + "\n")
    
    demo.launch(**launch_kwargs)
