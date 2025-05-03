# VoiceQuery

A Python application that transcribes voice to text using OpenAI's Whisper model, with future plans to process transcribed text into structured queries using language models.

## Features

- Upload audio files for transcription
- Record audio in real-time
- Transcribe audio to text using Whisper
- Multiple model size options (tiny, base, small, medium, large)
- Support for multiple languages
- User-friendly interface built with Gradio

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure you have FFmpeg installed on your system
   - On Ubuntu: `sudo apt-get install ffmpeg`
   - On macOS: `brew install ffmpeg`
   - On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

There are multiple ways to run the application:

### Using the run.py script (recommended)

```bash
./run.py
```

Optional arguments:
- `--port PORT`: Port to run the Gradio interface on (default: 7860)
- `--host HOST`: Host to run the Gradio interface on (default: 0.0.0.0)
- `--share`: Create a public link for the interface
- `--debug`: Run in debug mode

Example:
```bash
./run.py --port 8000 --share
```

### Using app.py directly

```bash
python app.py
```

### Using the modules directly

See the examples in the `examples/` directory for how to use the modules directly in your code.

Example:
```python
from utils.audio_processing import load_audio
from utils.transcription import WhisperTranscriber

# Load the transcriber
transcriber = WhisperTranscriber(model_name="base")

# Load and preprocess an audio file
audio_data = load_audio("path/to/audio.mp3")

# Transcribe the audio
result = transcriber.transcribe(audio_data)
print(result.text)
```

## Project Structure

- `app.py`: Main application entry point with Gradio interface
- `run.py`: Launcher script with command-line options
- `utils/`: Utility functions for audio processing and transcription
  - `audio_processing.py`: Functions for loading and processing audio
  - `transcription.py`: Functions for transcribing audio with Whisper
- `models/`: Model configurations
- `configs/`: Configuration files
  - `whisper_config.py`: Configuration for Whisper models
- `tests/`: Unit tests
- `examples/`: Usage examples

## Development

### Testing

Run the tests with pytest:

```bash
pytest
```

### Future Development

- Phase 1: Enhance the transcription features
  - Add support for batch processing
  - Implement caching for transcriptions
  - Support for exporting results

- Phase 2: Implement query generation
  - Integrate with language models
  - Process transcribed text into structured queries
  - Extend the UI to display both transcription and queries

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech-to-text model
- [Gradio](https://www.gradio.app/) for the web interface
- [EnkrateiaLucca](https://github.com/EnkrateiaLucca/audio_transcription_app_version_2) and [xAlpharax](https://github.com/xAlpharax/whisper-stt-gradio) for reference implementations 