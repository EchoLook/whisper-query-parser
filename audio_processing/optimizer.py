"""
Module for optimizing the processing of large audio files.
"""
import numpy as np
import torch
from pathlib import Path
import logging
from typing import List, Tuple, Dict, Optional, Union

logger = logging.getLogger(__name__)

def split_audio(audio_array: np.ndarray, sample_rate: int, 
               segment_length_sec: int = 30) -> List[np.ndarray]:
    """
    Splits an audio array into smaller segments for optimized processing.
    
    Args:
        audio_array: Complete audio array
        sample_rate: Audio sample rate
        segment_length_sec: Length of each segment in seconds
        
    Returns:
        List of segmented audio arrays
    """
    # Calculate the number of samples per segment
    segment_length = segment_length_sec * sample_rate
    
    # Calculate the number of complete segments
    num_segments = len(audio_array) // segment_length
    
    # Create list of segments
    segments = []
    
    for i in range(num_segments):
        start = i * segment_length
        end = (i + 1) * segment_length
        segments.append(audio_array[start:end])
    
    # Add the last segment if there's any remaining
    if len(audio_array) % segment_length > 0:
        segments.append(audio_array[num_segments * segment_length:])
    
    logger.info(f"Audio split into {len(segments)} segments")
    return segments

def optimize_whisper_config(file_size_mb: float) -> Dict[str, any]:
    """
    Adjusts Whisper configuration based on file size.
    
    Args:
        file_size_mb: File size in MB
        
    Returns:
        Dictionary with optimized configurations for Whisper
    """
    config = {
        "batch_size": 16,
        "compute_type": "float16",
        "beam_size": 5
    }
    
    # Adjust configuration based on file size
    if file_size_mb > 100:
        # For very large files, reduce precision to gain speed
        config["batch_size"] = 8
        config["compute_type"] = "int8"
        config["beam_size"] = 3
    elif file_size_mb > 50:
        # For medium-sized files
        config["batch_size"] = 12
        config["compute_type"] = "float16"
        config["beam_size"] = 4
    
    return config

def manage_memory(func):
    """
    Decorator to manage memory during audio processing.
    Frees GPU/CPU memory after processing.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # Clean torch memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Suggest to the garbage collector to free memory
        import gc
        gc.collect()
        
        return result
    
    return wrapper 