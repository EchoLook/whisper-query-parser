# whisper-query-parser

An application for transcribing voice to text using Whisper and generating structured queries with Gemini.

## Features

- **Speech-to-Text** - Transcribe uploaded audio files or record directly using your microphone
- **Multiple Languages** - Support for various languages with automatic language detection
- **Configurable Models** - Choose from different Whisper model sizes based on accuracy/speed needs
- **Query Generation** - Generate structured API queries from natural language using Gemini AI
- **Image Context** - Include images as reference for context-aware query generation
- **Responsive UI** - User-friendly interface built with Gradio
- **REST API** - Access all functionality through a RESTful API for integration with other services

## Setup

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whisper-query-parser.git
   cd whisper-query-parser
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

### Web Interface

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

### API

whisper-query-parser also provides a REST API that allows integration with other applications and services.

1. Start the API server:
   ```bash
   python api_run.py
   ```

2. The API server will be available at http://localhost:8000 (configurable through arguments or environment variables)

3. API Endpoints:
   - `GET /` - Basic API information
   - `POST /transcribe` - Transcribe an audio file
   - `POST /generate-query` - Generate a structured query from transcribed text
   - `POST /process` - Process audio file and optional image into a structured query

4. API Documentation:
   - Interactive API documentation available at http://localhost:8000/docs
   - ReDoc version available at http://localhost:8000/redoc

#### Example API Usage

##### Transcribe Audio

```bash
curl -X POST "http://localhost:8000/transcribe" \
  -H "accept: application/json" \
  -F "audio_file=@your_audio.wav" \
  -F "language=en"
```

Response:
```json
{
  "success": true,
  "transcription": "Text transcribed from the audio file"
}
```

##### Generate Query from Transcription

```bash
curl -X POST "http://localhost:8000/generate-query" \
  -H "accept: application/json" \
  -F "transcription=Me gustaría una camiseta azul de manga corta" \
  -F "image=@reference_image.jpg"
```

Response:
```json
{
  "success": true,
  "transcription": "Me gustaría una camiseta azul de manga corta",
  "query": {
    "items": [
      {
        "description": "camiseta azul manga corta",
        "max_price": null
      }
    ]
  }
}
```

##### Full Processing (Audio to Query)

```bash
curl -X POST "http://localhost:8000/process" \
  -H "accept: application/json" \
  -F "audio_file=@your_audio.wav" \
  -F "image=@reference_image.jpg" \
  -F "language=es"
```

Response:
```json
{
  "success": true,
  "transcription": "Me gustaría una camiseta azul de manga corta",
  "query": {
    "items": [
      {
        "description": "camiseta azul manga corta",
        "max_price": null
      }
    ]
  }
}
```

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
- **API connection issues**: Check that you're connecting to the correct port and that the API server is running.

## License

[MIT License](LICENSE)

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for speech-to-text capabilities
- [Google Gemini](https://ai.google.dev/docs/gemini_api_overview) for query generation
- [Gradio](https://www.gradio.app/) for the user interface
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework

## Project Structure

- `app.py`: Main application entry point with Gradio interface
- `run.py`: Launcher script with command-line options for the web interface
- `api.py`: FastAPI implementation for the REST API
- `api_run.py`: Launcher script for the API server
- `utils/`: Utility functions for audio processing and transcription
  - `audio_processing.py`: Functions for loading and processing audio
  - `transcription.py`: Functions for transcribing audio with Whisper
  - `query_generation.py`: Functions for generating structured queries
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

- Phase 3: API and Services
  - Optimize API performance
  - Add authentication and rate limiting
  - Develop client libraries for common languages

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech-to-text model
- [Gradio](https://www.gradio.app/) for the web interface
- [EnkrateiaLucca](https://github.com/EnkrateiaLucca/audio_transcription_app_version_2) and [xAlpharax](https://github.com/xAlpharax/whisper-stt-gradio) for reference implementations 