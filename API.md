# VoiceQuery API Documentation

This document provides a comprehensive guide to using the VoiceQuery API for speech transcription and structured query generation.

## Overview

The VoiceQuery API allows you to:

1. Transcribe audio files to text using OpenAI's Whisper model
2. Generate structured queries from transcribed text using Google's Gemini AI
3. Process audio and images directly into structured queries in a single API call

## Getting Started

### Prerequisites

- A running instance of the VoiceQuery API server
- Audio files for transcription (WAV, MP3, etc.)
- Optional image files for context (JPEG, PNG)
- An HTTP client for making API requests (e.g., curl, Python requests)

### Starting the API Server

```bash
python api_run.py --host 0.0.0.0 --port 8000
```

This will start the API server on the specified host and port.

Command-line options:
- `--host`: Host address to bind to (default: 0.0.0.0)
- `--port`: Port number to use (default: 8000)
- `--reload`: Enable auto-reload for development
- `--workers`: Number of worker processes (default: 1)

## API Endpoints

### Health Check

```
GET /health
```

Returns information about the API server's health and configuration.

**Example Response:**
```json
{
  "status": "healthy",
  "uptime": 123.45,
  "whisper_model": "base",
  "query_generation_available": true,
  "version": "1.0.0"
}
```

### Transcribe Audio

```
POST /transcribe
```

Transcribe an audio file to text.

**Parameters:**
- `audio_file` (file, required): The audio file to transcribe
- `language` (string, optional): Language code (e.g., "en", "es", "auto-detect")

**Example Request:**
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio_file=@your_audio.wav" \
  -F "language=en"
```

**Example Response:**
```json
{
  "success": true,
  "transcription": "I'm looking for a blue t-shirt with a logo on the front."
}
```

### Generate Query

```
POST /generate-query
```

Generate a structured query from transcribed text.

**Parameters:**
- `transcription` (string, required): The transcribed text
- `image` (file, optional): Reference image file

**Example Request:**
```bash
curl -X POST "http://localhost:8000/generate-query" \
  -F "transcription=I'm looking for a blue t-shirt with a logo on the front." \
  -F "image=@reference_image.jpg"
```

**Example Response:**
```json
{
  "success": true,
  "transcription": "I'm looking for a blue t-shirt with a logo on the front.",
  "query": {
    "items": [
      {
        "description": "blue t-shirt with logo on front",
        "max_price": null
      }
    ]
  }
}
```

### Process Audio to Query

```
POST /process
```

Process an audio file (and optional image) directly into a structured query.

**Parameters:**
- `audio_file` (file, required): The audio file to transcribe
- `image` (file, optional): Reference image file
- `language` (string, optional): Language code (e.g., "en", "es", "auto-detect")

**Example Request:**
```bash
curl -X POST "http://localhost:8000/process" \
  -F "audio_file=@your_audio.wav" \
  -F "image=@reference_image.jpg" \
  -F "language=en"
```

**Example Response:**
```json
{
  "success": true,
  "transcription": "I'm looking for a blue t-shirt with a logo on the front.",
  "query": {
    "items": [
      {
        "description": "blue t-shirt with logo on front",
        "max_price": null
      }
    ]
  }
}
```

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "transcription": null,
  "query": null
}
```

Common error status codes:
- `400`: Bad Request - Missing or invalid parameters
- `422`: Validation Error - Request validation failed
- `500`: Internal Server Error - Unexpected error during processing
- `503`: Service Unavailable - Query generation not available (missing API key)

## Example Client

A Python client example is provided in `examples/api_client.py` that demonstrates how to use the API:

```bash
python examples/api_client.py --audio your_audio.wav --image reference_image.jpg --language en
```

Command-line options:
- `--url`: Base URL of the API (default: http://localhost:8000)
- `--audio`: Path to the audio file (required)
- `--image`: Path to a reference image (optional)
- `--language`: Language code (optional)
- `--mode`: Operation mode (choices: "transcribe", "full", "separate"; default: "full")

## File Format Support

The API supports various audio and image formats:

**Audio Formats:**
- WAV
- MP3
- FLAC
- OGG
- M4A

**Image Formats:**
- JPEG/JPG
- PNG
- BMP
- GIF (first frame only)

## Limitations and Recommendations

- **Audio Length**: For optimal performance, audio files should be less than 10 minutes long
- **Audio Quality**: Clear audio with minimal background noise produces the best transcriptions
- **Image Context**: When using images, ensure they clearly show the relevant fashion items
- **Query Complexity**: The structured queries work best for clearly articulated fashion requests

## Integration Examples

### JavaScript/Node.js

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const apiUrl = 'http://localhost:8000';
const audioFile = 'path/to/audio.wav';
const imageFile = 'path/to/image.jpg';

async function processAudioToQuery() {
  const form = new FormData();
  form.append('audio_file', fs.createReadStream(audioFile));
  form.append('image', fs.createReadStream(imageFile));
  form.append('language', 'en');
  
  try {
    const response = await axios.post(`${apiUrl}/process`, form, {
      headers: form.getHeaders()
    });
    
    console.log('Transcription:', response.data.transcription);
    console.log('Query:', JSON.stringify(response.data.query, null, 2));
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

processAudioToQuery();
```

### Python

```python
import requests

api_url = 'http://localhost:8000'
audio_file = 'path/to/audio.wav'
image_file = 'path/to/image.jpg'

def process_audio_to_query():
    files = {
        'audio_file': open(audio_file, 'rb'),
        'image': open(image_file, 'rb')
    }
    data = {'language': 'en'}
    
    try:
        response = requests.post(
            f"{api_url}/process",
            files=files,
            data=data
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"Transcription: {result['transcription']}")
        print(f"Query: {result['query']}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    finally:
        for f in files.values():
            f.close()

process_audio_to_query()
``` 