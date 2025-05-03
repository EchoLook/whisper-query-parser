"""
Utility functions for audio transcription using Whisper.
"""
from typing import Dict, Optional, Union

import whisper  # This is the correct import
from pydantic import BaseModel

from utils.audio_processing import AudioData


class TranscriptionResult(BaseModel):
    """Model for transcription results."""
    text: str
    language: Optional[str] = None
    segments: Optional[list] = None
    duration: float


class WhisperTranscriber:
    """Class for handling transcription with Whisper models."""
    
    # Available models from smallest to largest
    AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large"]
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the transcriber with a specific Whisper model.
        
        Args:
            model_name (str): Name of the Whisper model to use (default: "base").
                              Options: "tiny", "base", "small", "medium", "large"
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model {model_name} not found. Available models: {self.AVAILABLE_MODELS}")
        
        self.model_name = model_name
        # Load the model
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio: Union[str, AudioData], language: Optional[str] = None) -> TranscriptionResult:
        """
        Transcribe audio to text.
        
        Args:
            audio (Union[str, AudioData]): Audio file path or AudioData object.
            language (Optional[str]): Language code for transcription (if known).
                                      If None, Whisper will detect the language.
        
        Returns:
            TranscriptionResult: Transcription results including text, language, etc.
        """
        # Prepare audio data
        if isinstance(audio, str):
            audio_path = audio
        else:  # AudioData object
            audio_path = audio.file_path if audio.file_path else None
            if audio_path is None:
                raise ValueError("AudioData object must have a file_path or provide numpy array for transcription")
        
        # Set transcription options
        options = {}
        
        # Handle language option properly
        if language and language.lower() != "auto-detect" and language != "None":
            options["language"] = language
        
        # Transcribe audio
        try:
            result = self.model.transcribe(audio_path, **options)
        except Exception as e:
            # If there's an error with language, try again with auto-detection
            if "language" in str(e).lower():
                result = self.model.transcribe(audio_path)
            else:
                raise
        
        # Create and return the result object
        return TranscriptionResult(
            text=result["text"],
            language=result.get("language"),
            segments=result.get("segments"),
            duration=result.get("duration", 0.0)
        ) 