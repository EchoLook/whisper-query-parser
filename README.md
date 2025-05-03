# VoiceQuery

An application for transcribing voice to text using Whisper and generating structured queries with Gemini.

## Features

- **Speech-to-Text** - Transcribe uploaded audio files or record directly using your microphone
- **Multiple Languages** - Support for various languages with automatic language detection
- **Configurable Models** - Choose from different Whisper model sizes based on accuracy/speed needs
- **Query Generation** - Generate structured API queries from natural language using Gemini AI
- **Image Context** - Include images as reference for context-aware query generation
- **Responsive UI** - User-friendly interface built with Gradio

## Setup

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/VoiceQuery.git
   cd VoiceQuery
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy the `.env.example` file to `.env`
   ```bash
   cp .env.example .env
   ```
   - Edit the `.env` file and add your Google API key for Gemini:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (typically http://127.0.0.1:7860)

3. Using the interface:
   - Select a Whisper model (tiny, base, small, medium, large)
   - Choose a language or use auto-detect
   - Upload a reference image if needed (for both tabs)
   - Either upload an audio file or record with your microphone
   - Click "Transcribe" to get the text result
   - Click "Generate Structured Query" to create a JSON query

### Example Use Cases

#### Fashion E-Commerce

Speech: "Me gusta el conjunto pero quiero una camiseta azul en vez de rosa y me gustaría que fuera barata"

Generated Query:
```json
{
  "items": [
    {
      "product_type": "camiseta",
      "color": "azul",
      "price_range": {
        "min": 0,
        "max": 20
      }
    }
  ]
}
```

Speech with Image: "El vestido es chulo pero no me convence, vamos a probar con unos vaqueros y una camiseta del mismo color"

Generated Query:
```json
{
  "items": [
    {
      "product_type": "vaqueros"
    },
    {
      "product_type": "camiseta",
      "color": "same as dress in image"
    }
  ]
}
```

## Troubleshooting

- **Query generation not working**: Make sure you have set up the `GOOGLE_API_KEY` environment variable with a valid API key.
- **Audio processing error**: Check that FFmpeg is installed on your system.
- **Memory issues with large models**: Try using a smaller Whisper model or split large audio files into smaller segments.

## License

[MIT License](LICENSE)

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text capabilities
- [Google Gemini](https://ai.google.dev/docs/gemini_api_overview) for query generation
- [Gradio](https://www.gradio.app/) for the user interface

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