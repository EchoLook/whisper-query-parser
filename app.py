"""
VoiceQuery - Voice to Text Application using Whisper.

This application provides a Gradio-based interface for transcribing
speech to text using OpenAI's Whisper model.
"""
import os
import tempfile
from typing import Dict, Optional, Tuple

import gradio as gr
import numpy as np

from utils.audio_processing import load_audio, preprocess_recorded_audio
from utils.transcription import WhisperTranscriber


# Initialize the transcriber with the base model
# Users can later select a different model in the interface
transcriber = WhisperTranscriber(model_name="base")


def transcribe_audio_file(audio_file: str, model_name: str, language: Optional[str] = None) -> str:
    """
    Transcribe an uploaded audio file.
    
    Args:
        audio_file (str): Path to the audio file.
        model_name (str): Name of the Whisper model to use.
        language (Optional[str]): Language code for transcription (if known).
    
    Returns:
        str: Transcribed text.
    """
    # Check if the file exists
    if audio_file is None or not audio_file or not os.path.exists(audio_file):
        return "Error: No se ha subido ningún archivo de audio válido."
    
    try:
        # Reload the model if different from current
        global transcriber
        if transcriber.model_name != model_name:
            transcriber = WhisperTranscriber(model_name=model_name)
        
        # Load and preprocess the audio
        audio_data = load_audio(audio_file)
        
        # Transcribe the audio
        result = transcriber.transcribe(audio_data, language=language)
        
        return result.text
    except Exception as e:
        return f"Error durante la transcripción: {str(e)}"


def transcribe_recorded_audio(audio_data: Tuple[int, np.ndarray], model_name: str, language: Optional[str] = None) -> str:
    """
    Transcribe recorded audio.
    
    Args:
        audio_data (Tuple[int, np.ndarray]): Tuple containing sample rate and audio array.
        model_name (str): Name of the Whisper model to use.
        language (Optional[str]): Language code for transcription (if known).
    
    Returns:
        str: Transcribed text.
    """
    # Verify that audio data exists
    if audio_data is None or not isinstance(audio_data, tuple) or len(audio_data) != 2:
        return "Error: No se ha grabado audio. Por favor, grabe audio antes de transcribir."
    
    sample_rate, audio_array = audio_data
    
    # Check if the audio array is empty or contains only silence
    if audio_array is None or len(audio_array) == 0 or np.max(np.abs(audio_array)) < 0.01:
        return "Error: El audio grabado está vacío o es demasiado silencioso. Por favor, grabe de nuevo."
    
    # Reload the model if different from current
    global transcriber
    try:
        if transcriber.model_name != model_name:
            transcriber = WhisperTranscriber(model_name=model_name)
        
        # Save recorded audio to a temporary file
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, "recorded_audio.wav")
        
        import soundfile as sf
        sf.write(temp_file_path, audio_array, sample_rate)
        
        # Transcribe the audio
        result = transcriber.transcribe(temp_file_path, language=language)
        
        return result.text
    except Exception as e:
        return f"Error durante la transcripción: {str(e)}"


def create_gradio_interface():
    """
    Create and configure the Gradio interface.
    
    Returns:
        gr.Blocks: Configured Gradio interface.
    """
    # Define available models and languages
    available_models = ["tiny", "base", "small", "medium", "large"]
    languages = [
        "auto-detect", "en", "es", "fr", "de", "it", "pt", "nl", "ru", 
        "zh", "ja", "ar", "hi", "ko", "tr", "pl"
    ]
    language_names = [
        "Auto-detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", 
        "Dutch", "Russian", "Chinese", "Japanese", "Arabic", "Hindi", "Korean", "Turkish", "Polish"
    ]
    
    with gr.Blocks(title="VoiceQuery - Voice to Text") as interface:
        gr.Markdown("# 🎙️ VoiceQuery: Voice to Text with Whisper")
        gr.Markdown("""
        Upload an audio file or record your voice to transcribe it to text using OpenAI's Whisper model.
        """)
        
        with gr.Row():
            with gr.Column():
                model_dropdown = gr.Dropdown(
                    choices=available_models,
                    value="base",
                    label="Whisper Model",
                    info="Larger models are more accurate but slower"
                )
                language_dropdown = gr.Dropdown(
                    choices=dict(zip(language_names, languages)),
                    value="Auto-detect",
                    label="Language",
                    info="Choose the language or leave as Auto-detect"
                )
        
        with gr.Tabs():
            with gr.TabItem("Upload Audio"):
                audio_file = gr.Audio(type="filepath", label="Upload Audio File")
                upload_button = gr.Button("Transcribe Uploaded Audio")
                upload_output = gr.Textbox(label="Transcription Result", lines=8)
                
                upload_button.click(
                    fn=transcribe_audio_file,
                    inputs=[audio_file, model_dropdown, language_dropdown],
                    outputs=upload_output
                )
            
            with gr.TabItem("Record Audio"):
                audio_recorder = gr.Audio(
                    sources=["microphone"], 
                    type="numpy", 
                    label="Record Audio",
                    interactive=True
                )
                record_button = gr.Button("Transcribe Recorded Audio")
                record_output = gr.Textbox(label="Transcription Result", lines=8)
                
                record_button.click(
                    fn=transcribe_recorded_audio,
                    inputs=[audio_recorder, model_dropdown, language_dropdown],
                    outputs=record_output
                )
                
                # Add a clear button for the recorder
                clear_button = gr.Button("Clear Recorder")
                clear_button.click(
                    fn=lambda: None,
                    inputs=[],
                    outputs=[audio_recorder, record_output]
                )
        
        # Add a status message area
        status = gr.Markdown("")
        
        gr.Markdown("""
        ## 📋 How to Use
        1. Select a Whisper model (larger models are more accurate but slower)
        2. Optionally select a language (or leave as Auto-detect)
        3. Either upload an audio file or record your voice
        4. Click the "Transcribe" button to get the text result
        
        ## ℹ️ About
        This application uses OpenAI's Whisper model to transcribe speech to text. 
        It supports multiple languages and different model sizes for various accuracy/speed trade-offs.
        """)
    
    return interface


if __name__ == "__main__":
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(share=False) 