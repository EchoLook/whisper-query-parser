"""
Utility functions for audio processing and preparation for transcription.
"""
import os
import tempfile
from typing import Optional, Tuple

import librosa
import numpy as np
from pydantic import BaseModel
from pydub import AudioSegment


class AudioData(BaseModel):
    """Model for processed audio data."""
    sample_rate: int
    audio_array: np.ndarray
    duration: float
    file_path: Optional[str] = None
    
    model_config = {
        "arbitrary_types_allowed": True
    }


def load_audio(file_path: str) -> AudioData:
    """
    Load an audio file and preprocess it for transcription.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        AudioData: Preprocessed audio data.
    """
    # Load audio file
    audio_array, sample_rate = librosa.load(file_path, sr=16000)
    
    # Get duration
    duration = librosa.get_duration(y=audio_array, sr=sample_rate)
    
    return AudioData(
        sample_rate=sample_rate,
        audio_array=audio_array,
        duration=duration,
        file_path=file_path
    )


def save_audio_from_bytes(audio_bytes: bytes, file_format: str = "wav") -> str:
    """
    Save audio bytes to a temporary file.

    Args:
        audio_bytes (bytes): Audio data in bytes.
        file_format (str): Format of the audio file (default: "wav").

    Returns:
        str: Path to the saved temporary file.
    """
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, f"recorded_audio.{file_format}")
    
    with open(temp_file_path, "wb") as f:
        f.write(audio_bytes)
    
    return temp_file_path


def preprocess_recorded_audio(audio_bytes: bytes) -> AudioData:
    """
    Preprocess recorded audio from bytes for transcription.

    Args:
        audio_bytes (bytes): Audio data in bytes.

    Returns:
        AudioData: Preprocessed audio data.
    """
    # Save bytes to temporary file
    temp_file_path = save_audio_from_bytes(audio_bytes)
    
    # Load and process the audio
    return load_audio(temp_file_path) 