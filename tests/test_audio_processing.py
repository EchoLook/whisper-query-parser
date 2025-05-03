"""
Unit tests for the audio processing module.
"""
import os
import tempfile
from unittest import mock

import numpy as np
import pytest

from utils.audio_processing import AudioData, load_audio, preprocess_recorded_audio, save_audio_from_bytes


def test_audio_data_model():
    """Test the AudioData model."""
    # Create a valid AudioData object
    audio_data = AudioData(
        sample_rate=16000,
        audio_array=np.zeros(16000),
        duration=1.0,
        file_path="/tmp/test.wav"
    )
    
    # Check that the attributes are correctly set
    assert audio_data.sample_rate == 16000
    assert audio_data.audio_array.shape == (16000,)
    assert audio_data.duration == 1.0
    assert audio_data.file_path == "/tmp/test.wav"


@mock.patch("librosa.load")
@mock.patch("librosa.get_duration")
def test_load_audio(mock_get_duration, mock_load):
    """Test loading an audio file."""
    # Mock the librosa functions
    audio_array = np.zeros(16000)
    sample_rate = 16000
    duration = 1.0
    
    mock_load.return_value = (audio_array, sample_rate)
    mock_get_duration.return_value = duration
    
    # Load an audio file
    file_path = "/tmp/test.wav"
    audio_data = load_audio(file_path)
    
    # Check that the librosa functions were called with the correct parameters
    mock_load.assert_called_once_with(file_path, sr=16000)
    mock_get_duration.assert_called_once()
    
    # Check the result
    assert audio_data.sample_rate == sample_rate
    assert audio_data.duration == duration
    assert audio_data.file_path == file_path


def test_save_audio_from_bytes():
    """Test saving audio bytes to a temporary file."""
    # Create some test audio bytes
    audio_bytes = b"test audio data"
    
    # Save the audio bytes
    file_path = save_audio_from_bytes(audio_bytes)
    
    # Check that the file exists and contains the correct data
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        saved_data = f.read()
    assert saved_data == audio_bytes
    
    # Clean up
    os.remove(file_path)


@mock.patch("utils.audio_processing.save_audio_from_bytes")
@mock.patch("utils.audio_processing.load_audio")
def test_preprocess_recorded_audio(mock_load_audio, mock_save_audio):
    """Test preprocessing recorded audio."""
    # Mock the functions
    temp_file_path = "/tmp/recorded_audio.wav"
    mock_save_audio.return_value = temp_file_path
    
    expected_audio_data = AudioData(
        sample_rate=16000,
        audio_array=np.zeros(16000),
        duration=1.0,
        file_path=temp_file_path
    )
    mock_load_audio.return_value = expected_audio_data
    
    # Preprocess some test audio bytes
    audio_bytes = b"test audio data"
    audio_data = preprocess_recorded_audio(audio_bytes)
    
    # Check that the functions were called with the correct parameters
    mock_save_audio.assert_called_once_with(audio_bytes)
    mock_load_audio.assert_called_once_with(temp_file_path)
    
    # Check the result
    assert audio_data == expected_audio_data 