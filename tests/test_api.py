"""
Tests for the whisper-query-parser API endpoints.
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from api import app

# Create a test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns basic information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data

def test_transcribe_endpoint_validation():
    """Test transcribe endpoint validates input properly."""
    # Test without a file
    response = client.post("/transcribe")
    assert response.status_code == 422  # Validation error

    # Test with empty file data
    response = client.post(
        "/transcribe",
        files={"audio_file": ("empty.wav", b"", "audio/wav")}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "error" in data

@pytest.mark.skipif(not os.path.exists("examples/test_audio.wav"), 
                    reason="Test audio file not found")
def test_transcribe_with_test_file():
    """Test transcription with a real audio file if available."""
    test_file_path = Path("examples/test_audio.wav")
    if test_file_path.exists():
        with open(test_file_path, "rb") as f:
            response = client.post(
                "/transcribe",
                files={"audio_file": ("test_audio.wav", f, "audio/wav")},
                data={"language": "en"}
            )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "transcription" in data
        assert len(data["transcription"]) > 0

def test_generate_query_endpoint_validation():
    """Test generate-query endpoint validates input properly."""
    # Test without transcription
    response = client.post("/generate-query")
    assert response.status_code == 422  # Validation error
    
    # Test with empty transcription
    response = client.post(
        "/generate-query",
        data={"transcription": ""}
    )
    assert response.status_code == 200  # This should succeed but may have error in content
    data = response.json()
    assert "query" in data

def test_process_endpoint_validation():
    """Test process endpoint validates input properly."""
    # Test without a file
    response = client.post("/process")
    assert response.status_code == 422  # Validation error

    # Test with empty file data
    response = client.post(
        "/process",
        files={"audio_file": ("empty.wav", b"", "audio/wav")}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "error" in data 