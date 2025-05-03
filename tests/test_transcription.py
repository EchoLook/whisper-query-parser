"""
Unit tests for the transcription module.
"""
import os
import tempfile
from unittest import mock

import numpy as np
import pytest

from utils.audio_processing import AudioData
from utils.transcription import TranscriptionResult, WhisperTranscriber


def test_transcription_result_model():
    """Test the TranscriptionResult model."""
    # Create a valid TranscriptionResult object
    result = TranscriptionResult(
        text="Hello world",
        language="en",
        segments=[{"text": "Hello world", "start": 0.0, "end": 1.0}],
        duration=1.0
    )
    
    # Check that the attributes are correctly set
    assert result.text == "Hello world"
    assert result.language == "en"
    assert len(result.segments) == 1
    assert result.duration == 1.0


def test_whisper_transcriber_invalid_model():
    """Test that WhisperTranscriber raises an error for invalid models."""
    # Try to initialize with an invalid model name
    with pytest.raises(ValueError):
        WhisperTranscriber(model_name="invalid_model")


@mock.patch("whisper.load_model")
def test_whisper_transcriber_initialization(mock_load_model):
    """Test WhisperTranscriber initialization."""
    # Mock the whisper.load_model function
    mock_model = mock.MagicMock()
    mock_load_model.return_value = mock_model
    
    # Initialize the transcriber
    transcriber = WhisperTranscriber(model_name="base")
    
    # Check that the model was loaded with the correct name
    mock_load_model.assert_called_once_with("base")
    assert transcriber.model_name == "base"
    assert transcriber.model == mock_model


@mock.patch("whisper.load_model")
def test_transcribe_with_audio_data(mock_load_model):
    """Test transcribing with AudioData object."""
    # Create a mock model and result
    mock_model = mock.MagicMock()
    mock_model.transcribe.return_value = {
        "text": "This is a test",
        "language": "en",
        "segments": [],
        "duration": 2.0
    }
    mock_load_model.return_value = mock_model
    
    # Create a test audio data object
    audio_data = AudioData(
        sample_rate=16000,
        audio_array=np.zeros(16000),
        duration=1.0,
        file_path="/tmp/test.wav"
    )
    
    # Initialize the transcriber and transcribe
    transcriber = WhisperTranscriber(model_name="base")
    result = transcriber.transcribe(audio_data)
    
    # Check that the model was called with the correct parameters
    mock_model.transcribe.assert_called_once_with(audio_data.file_path)
    
    # Check the result
    assert result.text == "This is a test"
    assert result.language == "en"
    assert result.duration == 2.0


@mock.patch("whisper.load_model")
def test_transcribe_with_language(mock_load_model):
    """Test transcribing with a specified language."""
    # Create a mock model and result
    mock_model = mock.MagicMock()
    mock_model.transcribe.return_value = {
        "text": "Esto es una prueba",
        "language": "es",
        "segments": [],
        "duration": 2.0
    }
    mock_load_model.return_value = mock_model
    
    # Initialize the transcriber and transcribe
    transcriber = WhisperTranscriber(model_name="base")
    result = transcriber.transcribe("/tmp/test.wav", language="es")
    
    # Check that the model was called with the correct parameters
    mock_model.transcribe.assert_called_once_with("/tmp/test.wav", language="es")
    
    # Check the result
    assert result.text == "Esto es una prueba"
    assert result.language == "es"
    assert result.duration == 2.0 