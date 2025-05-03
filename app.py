"""
whisper-query-parser - Voice to Text Application using Whisper.

This application provides a Gradio-based interface for transcribing
speech to text using OpenAI's Whisper model and generating structured queries
using Google's Gemini model.
"""
import os
import tempfile
from typing import Dict, Optional, Tuple, Union
from pathlib import Path
import json
from dotenv import load_dotenv

import gradio as gr
import numpy as np
from gradio.themes.utils import colors, fonts, sizes
from gradio.themes import Base
from PIL import Image
import whisper

from utils.audio_processing import load_audio, preprocess_recorded_audio
from utils.transcription import WhisperTranscriber
from utils.query_generation import QueryGenerator
from audio_processing.optimizer import split_audio, optimize_whisper_config, manage_memory
from export.transcript_exporter import TranscriptExporter

# Load environment variables from .env file
load_dotenv()

# Initialize the transcriber with the base model from .env or default to "base"
model_name = os.getenv("WHISPER_MODEL", "base")
transcriber = WhisperTranscriber(model_name=model_name)

# Instanciar el exportador
export_dir = os.getenv("EXPORT_DIR", "exports")
exporter = TranscriptExporter(export_dir=export_dir)

# Cargar modelo de Whisper
model = whisper.load_model(model_name)

# Initialize QueryGenerator (will use API key from .env)
try:
    query_generator = QueryGenerator()
except ValueError:
    query_generator = None
    print("Warning: Google API key not found in .env file. Query generation will be disabled.")
    print("Add GOOGLE_API_KEY=your_key to your .env file to enable query generation.")


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


def generate_query_from_transcript(transcript: str, image: Optional[Union[str, Image.Image]] = None) -> str:
    """
    Generate a structured query from transcribed text using Gemini.
    
    Args:
        transcript: The transcribed speech text
        image: Optional image path or image object
        
    Returns:
        Formatted JSON string with the structured query
    """
    if not transcript or transcript.strip() == "":
        return json.dumps({"error": "No text to process."}, indent=2)
    
    # Handle missing query generator (API key not configured)
    global query_generator
    if query_generator is None:
        return json.dumps({
            "error": "Query generation is not available. Please set the GOOGLE_API_KEY environment variable and restart the application."
        }, indent=2)
    
    # Handle the image input
    image_path = None
    if image is not None:
        # If image is a filepath string
        if isinstance(image, str) and os.path.exists(image):
            image_path = image
        # If image is uploaded through Gradio
        elif hasattr(image, 'name') and os.path.exists(image.name):
            image_path = image.name
        # If image is a PIL Image
        elif isinstance(image, Image.Image):
            # Save to temp file
            temp_dir = tempfile.gettempdir()
            image_path = os.path.join(temp_dir, "uploaded_image.jpg")
            image.save(image_path)
    
    try:
        return query_generator.generate_query_text(transcript, image_path)
    except Exception as e:
        return json.dumps({
            "error": f"Error generating query: {str(e)}",
            "transcript": transcript
        }, indent=2)


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
    
    # Definir un tema personalizado para la aplicación
    class VoiceQueryTheme(Base):
        def __init__(self):
            super().__init__(
                primary_hue=colors.indigo,
                secondary_hue=colors.purple,
                neutral_hue=colors.gray,
                font=(fonts.GoogleFont("Inter"), fonts.GoogleFont("IBM Plex Mono")),
                radius_size=sizes.radius_md,
            )
            # Personalización adicional
            self.button_primary_background_fill = "linear-gradient(90deg, *primary_500, *secondary_500)"
            self.button_primary_background_fill_hover = "linear-gradient(90deg, *primary_600, *secondary_600)"
            self.block_label_background_fill = "linear-gradient(90deg, *primary_100, *secondary_100)"
            self.block_title_text_weight = "600"

    with gr.Blocks(theme=VoiceQueryTheme()) as interface:
        gr.Markdown("# 🎙️ VoiceQuery: Voice to Text with Whisper + Gemini")
        gr.Markdown("""
        Upload an audio file or record your voice to transcribe it to text using OpenAI's Whisper model.
        Then generate structured queries for e-commerce API using Google's Gemini model.
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
        
        # Create a shared image input that will be used by both tabs
        shared_image = gr.Image(
            type="pil", 
            label="Upload Reference Image (Optional)",
            elem_id="shared_image"
        )
            
        with gr.Tabs() as tabs:
            with gr.TabItem("Upload Audio") as tab_upload:
                with gr.Row():
                    with gr.Column(scale=1):
                        audio_file = gr.Audio(type="filepath", label="Upload Audio File")
                        upload_button = gr.Button("Transcribe Uploaded Audio")
                
                upload_output = gr.Textbox(label="Transcription Result", lines=8)
                
                upload_button.click(
                    fn=transcribe_audio_file,
                    inputs=[audio_file, model_dropdown, language_dropdown],
                    outputs=upload_output
                )
                
                # Add query generation section
                query_button = gr.Button("Generate Structured Query")
                query_output = gr.JSON(label="Generated Query")
                
                query_button.click(
                    fn=generate_query_from_transcript,
                    inputs=[upload_output, shared_image],
                    outputs=query_output
                )
            
            with gr.TabItem("Record Audio") as tab_record:
                with gr.Row():
                    with gr.Column(scale=1):
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
                
                # Add query generation section for recorded audio
                query_button_record = gr.Button("Generate Structured Query")
                query_output_record = gr.JSON(label="Generated Query")
                
                query_button_record.click(
                    fn=generate_query_from_transcript,
                    inputs=[record_output, shared_image],
                    outputs=query_output_record
                )
                
                # Add a clear button for the recorder
                clear_button = gr.Button("Clear Recorder")
                clear_button.click(
                    fn=lambda: None,
                    inputs=[],
                    outputs=[audio_recorder, record_output, query_output_record]
                )
        
        # Add the shared image to both tabs using JavaScript
        # This ensures the image state is maintained when switching tabs
        gr.HTML("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Function to move the shared image element to the current tab
            function moveImageToTab() {
                const sharedImage = document.getElementById('shared_image').parentElement.parentElement;
                const activeTab = document.querySelector('.tabitem.selected');
                
                if (activeTab && sharedImage) {
                    const targetRow = activeTab.querySelector('.row');
                    if (targetRow) {
                        // Create or get the second column if it doesn't exist
                        let secondColumn = targetRow.querySelector('.col:nth-child(2)');
                        if (!secondColumn) {
                            secondColumn = document.createElement('div');
                            secondColumn.classList.add('col');
                            secondColumn.style.flex = '1 1 0%';
                            targetRow.appendChild(secondColumn);
                        }
                        
                        // Move the shared image to the second column
                        secondColumn.appendChild(sharedImage);
                    }
                }
            }
            
            // Move image on initial load
            setTimeout(moveImageToTab, 500);
            
            // Move image when tabs change
            const tabButtons = document.querySelectorAll('[id^="tab_"]');
            tabButtons.forEach(button => {
                button.addEventListener('click', function() {
                    setTimeout(moveImageToTab, 100);
                });
            });
        });
        </script>
        """)
        
        # Add a status message area
        status = gr.Markdown("")
        
        gr.Markdown("""
        ## 📋 How to Use
        1. Select a Whisper model (larger models are more accurate but slower)
        2. Optionally select a language (or leave as Auto-detect)
        3. Upload a reference image if needed (the image will be used for both tabs)
        4. Either upload an audio file or record your voice in the respective tab
        5. Click the "Transcribe" button to get the text result
        6. Click "Generate Structured Query" to create a JSON query based on the transcription
        
        ## ℹ️ About
        This application uses OpenAI's Whisper model to transcribe speech to text and Google's Gemini model to generate structured queries for e-commerce APIs. It supports multiple languages and can process both audio and image inputs to generate context-aware queries.
        """)
    
    return interface


@manage_memory
def transcribe_audio(audio_path: Union[str, Path], progress=gr.Progress()) -> Dict:
    """
    Transcribe audio using the Whisper model with optimizations for large files.
    
    Args:
        audio_path: Path to the audio file
        progress: Gradio Progress object to show progress
        
    Returns:
        Dictionary with the transcription result
    """
    audio_path = Path(audio_path)
    file_size_mb = audio_path.stat().st_size / (1024 * 1024)
    
    # Get optimized configuration
    whisper_config = optimize_whisper_config(file_size_mb)
    
    # For large files, process by segments
    if file_size_mb > 30:  # 30MB as threshold to consider "large"
        progress(0, desc="Loading audio...")
        # Load audio using whisper
        audio = whisper.load_audio(str(audio_path))
        
        progress(0.1, desc="Splitting into segments...")
        # Split into segments
        segments = split_audio(audio, sample_rate=16000, segment_length_sec=30)
        
        # Transcribe segments
        full_result = {"text": ""}
        
        for i, segment in enumerate(segments):
            progress_value = 0.1 + 0.9 * (i / len(segments))
            progress(progress_value, desc=f"Transcribing segment {i+1}/{len(segments)}...")
            
            # Transcribe segment
            result = model.transcribe(segment, **whisper_config)
            full_result["text"] += result["text"] + " "
    else:
        # For small files, transcribe directly
        progress(0.2, desc="Transcribing audio...")
        full_result = model.transcribe(str(audio_path), **whisper_config)
    
    progress(1.0, desc="Transcription completed!")
    return full_result


def export_transcript(transcript: str, format: str, include_metadata: bool = False) -> str:
    """
    Export the transcription in the specified format.
    
    Args:
        transcript: Text of the transcription
        format: Export format ('txt', 'json', 'csv')
        include_metadata: Include metadata in the export
        
    Returns:
        Message with the path of the exported file
    """
    metadata = None
    if include_metadata:
        metadata = {
            "model": "whisper-base",
            "format": format,
            "app_version": "1.0"
        }
    
    if format == "txt":
        path = exporter.export_as_text(transcript)
    elif format == "json":
        path = exporter.export_as_json(transcript, metadata)
    elif format == "csv":
        path = exporter.export_as_csv(transcript, metadata)
    else:
        return "Unsupported format"
    
    return f"Transcription exported to: {path}"


def send_to_ai(transcript: str) -> str:
    """
    Prepare and send the transcription to the AI (next phase).
    
    Args:
        transcript: Text of the transcription
        
    Returns:
        Confirmation message
    """
    metadata = {
        "source": "audio_transcript",
        "model": "whisper-base",
        "processing_time": "N/A"  # You could add actual processing time here
    }
    
    ai_data = exporter.prepare_for_ai(transcript, metadata)
    
    # Here you would implement the logic to send to the IA in the next phase
    # For now, we just generate a JSON file ready to use
    path = exporter.export_as_json(
        transcript, 
        metadata=metadata, 
        filename=f"ai_ready_{exporter._generate_filename(extension='json')}"
    )
    
    return f"Data prepared for IA and saved to: {path}"


if __name__ == "__main__":
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(share=False) 