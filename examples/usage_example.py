"""
Example of how to use the VoiceQuery modules directly.
"""
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.audio_processing import load_audio
from utils.transcription import WhisperTranscriber


def transcribe_from_file(file_path: str, model_name: str = "base", language: str = None) -> str:
    """
    Example function to transcribe audio from a file directly.
    
    Args:
        file_path (str): Path to the audio file.
        model_name (str): Name of the Whisper model to use.
        language (str): Optional language code for transcription.
    
    Returns:
        str: Transcribed text.
    """
    # Load the transcriber
    transcriber = WhisperTranscriber(model_name=model_name)
    
    # Load and preprocess the audio
    audio_data = load_audio(file_path)
    print(f"Loaded audio file: {file_path}, duration: {audio_data.duration:.2f} seconds")
    
    # Transcribe the audio
    result = transcriber.transcribe(audio_data, language=language)
    
    print(f"Transcription completed using model '{model_name}'")
    if result.language:
        print(f"Detected language: {result.language}")
    
    return result.text


if __name__ == "__main__":
    # Example usage
    
    # Replace with your actual audio file path
    sample_file = "path/to/your/audio/file.mp3"
    
    if len(sys.argv) > 1:
        sample_file = sys.argv[1]
    
    if not os.path.exists(sample_file):
        print(f"Error: File {sample_file} does not exist.")
        print("Usage: python usage_example.py [audio_file_path]")
        sys.exit(1)
    
    # Transcribe the audio
    text = transcribe_from_file(sample_file, model_name="base")
    
    print("\nTranscription Result:")
    print("-" * 40)
    print(text)
    print("-" * 40) 