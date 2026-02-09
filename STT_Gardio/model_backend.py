"""
Model backend for Whisper speech-to-text transcription.

This module provides a lazy-loaded transformers pipeline for automatic
speech recognition using the OpenAI Whisper large-v3-turbo model.
"""

import logging
import warnings
from typing import Dict, Optional, Any
from transformers import pipeline
import torch

# Suppress transformers warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", message=".*past_key_values.*")
warnings.filterwarnings("ignore", message=".*inputs.*deprecated.*")

# Configuration constants
MODEL_NAME = "openai/whisper-large-v3-turbo"
PIPELINE_TYPE = "automatic-speech-recognition"

# Module-level cache for the pipeline
_stt_pipeline: Optional[Any] = None

# Set up logging
logger = logging.getLogger(__name__)


def get_pipeline():
    """
    Lazy-load and return the cached STT pipeline.
    
    The pipeline is initialized on first call and cached for subsequent use.
    This avoids reloading the model on every transcription request.
    Automatically uses GPU if available, otherwise falls back to CPU.
    
    Returns:
        transformers.Pipeline: The automatic speech recognition pipeline.
    """
    global _stt_pipeline
    
    if _stt_pipeline is None:
        logger.info(f"Initializing {PIPELINE_TYPE} pipeline with model: {MODEL_NAME}")
        
        # Determine device: use GPU if available, otherwise CPU
        if torch.cuda.is_available():
            device = 0  # Use first GPU
            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = -1  # Use CPU
            logger.info("Using CPU (GPU not available)")
        
        try:
            _stt_pipeline = pipeline(
                PIPELINE_TYPE,
                model=MODEL_NAME,
                device=device
            )
            logger.info("Pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            raise
    
    return _stt_pipeline


def clear_cuda_cache():
    """
    Clear CUDA cache to free GPU memory.
    This should be called after each transcription to prevent memory buildup.
    """
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        logger.debug("CUDA cache cleared")


def transcribe_audio(audio_path: str) -> Dict[str, Any]:
    """
    Transcribe an audio file using the Whisper model.
    
    Args:
        audio_path: Path to the audio file to transcribe.
        
    Returns:
        A dictionary containing:
            - 'text': Full transcription string
            - 'language': Detected language code (if available)
            - 'segments': List of segments with timestamps (if available)
            - 'raw_output': Raw pipeline output for debugging
            
    Raises:
        FileNotFoundError: If the audio file doesn't exist.
        Exception: If transcription fails.
    """
    import os
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    logger.info(f"Transcribing audio file: {audio_path}")
    
    try:
        # Get the pipeline and run transcription
        # return_timestamps=True is required for audio longer than 30 seconds
        pipeline_instance = get_pipeline()
        result = pipeline_instance(audio_path, return_timestamps=True)
        
        # Handle different output formats from the pipeline
        # The pipeline can return:
        # 1. A dict with 'text' key
        # 2. A dict with 'text' and 'chunks' keys
        # 3. Just a string (older versions)
        
        if isinstance(result, str):
            # If result is just a string
            transcription_text = result
            language = None
            segments = None
        elif isinstance(result, dict):
            # Extract text
            transcription_text = result.get("text", "")
            
            # Extract language if available
            language = result.get("language", None)
            
            # Extract segments/chunks if available
            # When return_timestamps=True, the pipeline returns 'chunks' with timestamp info
            segments = result.get("chunks", None)
            
            # If chunks exist, format them properly for JSON output
            if segments is not None:
                # Format segments to include timestamp information
                formatted_segments = []
                for chunk in segments:
                    if isinstance(chunk, dict):
                        formatted_segments.append({
                            "text": chunk.get("text", ""),
                            "timestamp": chunk.get("timestamp", None)
                        })
                    else:
                        # Handle different chunk formats
                        formatted_segments.append(chunk)
                segments = formatted_segments
        else:
            # Unexpected format
            logger.warning(f"Unexpected pipeline output format: {type(result)}")
            transcription_text = str(result)
            language = None
            segments = None
        
        # Ensure we have text
        if not transcription_text:
            raise ValueError("Pipeline returned empty transcription")
        
        # Build normalized output
        output = {
            "text": transcription_text,
            "language": language,
            "segments": segments
        }
        
        logger.info(f"Transcription completed. Text length: {len(transcription_text)} characters")
        if language:
            logger.info(f"Detected language: {language}")
        
        return output
        
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise
    finally:
        # Always clear CUDA cache after transcription (success or failure)
        clear_cuda_cache()
