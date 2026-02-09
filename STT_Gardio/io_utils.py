"""
I/O utilities for generating downloadable files from transcription results.

This module provides functions to create temporary text and JSON files
from transcription output for user downloads.
"""

import json
import tempfile
import os
from typing import Dict, Any


def make_txt_file(text: str, prefix: str = "transcription") -> str:
    """
    Create a temporary .txt file containing the transcribed text.
    
    Args:
        text: The transcription text to write.
        prefix: Prefix for the temporary file name.
        
    Returns:
        Path to the created temporary file.
    """
    # Create a temporary file with .txt extension
    fd, file_path = tempfile.mkstemp(suffix=".txt", prefix=f"{prefix}_", text=True)
    
    try:
        # Write text as UTF-8
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return file_path
    except Exception as e:
        # Clean up file descriptor if writing fails
        os.close(fd)
        if os.path.exists(file_path):
            os.unlink(file_path)
        raise


def make_json_file(payload: Dict[str, Any], prefix: str = "transcription") -> str:
    """
    Create a temporary .json file containing the transcription data.
    
    Args:
        payload: Dictionary containing transcription data (text, language, segments, etc.).
        prefix: Prefix for the temporary file name.
        
    Returns:
        Path to the created temporary file.
    """
    # Create a temporary file with .json extension
    fd, file_path = tempfile.mkstemp(suffix=".json", prefix=f"{prefix}_", text=True)
    
    try:
        # Write JSON with pretty formatting
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        
        return file_path
    except Exception as e:
        # Clean up file descriptor if writing fails
        os.close(fd)
        if os.path.exists(file_path):
            os.unlink(file_path)
        raise
