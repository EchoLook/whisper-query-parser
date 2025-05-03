#!/usr/bin/env python3
"""
Example client for the whisper-query-parser API.

This script demonstrates how to interact with the whisper-query-parser API 
using Python's requests library.
"""
import os
import sys
import json
import argparse
from pathlib import Path
import requests


def check_api_health(base_url):
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{base_url}/health")
        response.raise_for_status()
        health_info = response.json()
        
        print(f"API Status: {health_info['status']}")
        print(f"API Version: {health_info['version']}")
        print(f"Uptime: {health_info['uptime']:.2f} seconds")
        print(f"Whisper Model: {health_info['whisper_model']}")
        print(f"Query Generation Available: {health_info['query_generation_available']}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return False


def transcribe_audio(base_url, audio_file_path, language=None):
    """
    Transcribe an audio file using the API.
    
    Args:
        base_url: The base URL of the API
        audio_file_path: Path to the audio file
        language: Optional language code
        
    Returns:
        The transcribed text if successful, None otherwise
    """
    print(f"\nTranscribing audio file: {audio_file_path}")
    
    # Prepare the files and data
    files = {"audio_file": open(audio_file_path, "rb")}
    data = {}
    if language:
        data["language"] = language
        
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/transcribe",
            files=files,
            data=data
        )
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            print(f"Transcription successful:")
            print(f"  Text: {result['transcription']}")
            return result["transcription"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    finally:
        files["audio_file"].close()


def generate_query(base_url, transcription, image_path=None):
    """
    Generate a structured query from transcribed text.
    
    Args:
        base_url: The base URL of the API
        transcription: The transcribed text
        image_path: Optional path to an image file
        
    Returns:
        The generated query JSON if successful, None otherwise
    """
    print(f"\nGenerating query from text: {transcription}")
    
    # Prepare the files and data
    files = {}
    if image_path:
        files["image"] = open(image_path, "rb")
        
    data = {"transcription": transcription}
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/generate-query",
            files=files,
            data=data
        )
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            print(f"Query generation successful:")
            print(json.dumps(result["query"], indent=2))
            return result["query"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    finally:
        if "image" in files:
            files["image"].close()


def process_audio_to_query(base_url, audio_file_path, image_path=None, language=None):
    """
    Process audio directly to a structured query in one API call.
    
    Args:
        base_url: The base URL of the API
        audio_file_path: Path to the audio file
        image_path: Optional path to an image file
        language: Optional language code
        
    Returns:
        Tuple of (transcription, query) if successful, (None, None) otherwise
    """
    print(f"\nProcessing audio to query: {audio_file_path}")
    
    # Prepare the files and data
    files = {"audio_file": open(audio_file_path, "rb")}
    if image_path:
        files["image"] = open(image_path, "rb")
        
    data = {}
    if language:
        data["language"] = language
        
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/process",
            files=files,
            data=data
        )
        response.raise_for_status()
        result = response.json()
        
        if result["success"]:
            print(f"Processing successful:")
            print(f"  Transcription: {result['transcription']}")
            print(f"  Query:")
            print(json.dumps(result["query"], indent=2))
            return result["transcription"], result["query"]
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None, None
    finally:
        for f in files.values():
            f.close()


def main():
    """Main entry point for the API client example."""
    parser = argparse.ArgumentParser(description="whisper-query-parser API Client Example")
    
    parser.add_argument(
        "--url", 
        type=str, 
        default="http://localhost:8000", 
        help="Base URL of the whisper-query-parser API"
    )
    
    parser.add_argument(
        "--audio", 
        type=str, 
        required=True, 
        help="Path to the audio file to transcribe"
    )
    
    parser.add_argument(
        "--image", 
        type=str, 
        help="Optional path to an image file for context"
    )
    
    parser.add_argument(
        "--language", 
        type=str, 
        help="Optional language code (e.g., 'en', 'es')"
    )
    
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["transcribe", "full", "separate"],
        default="full",
        help=(
            "Mode of operation: 'transcribe' for transcription only, "
            "'full' for direct audio-to-query, "
            "'separate' for separate transcription and query generation calls"
        )
    )
    
    args = parser.parse_args()
    
    # Validate paths
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: Audio file not found at {audio_path}")
        return 1
    
    image_path = None
    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image file not found at {image_path}")
            return 1
    
    # Check API health
    if not check_api_health(args.url):
        return 1
    
    # Execute the requested mode
    if args.mode == "transcribe":
        # Only perform transcription
        transcribe_audio(args.url, str(audio_path), args.language)
    
    elif args.mode == "full":
        # Use the combined endpoint
        process_audio_to_query(args.url, str(audio_path), 
                              str(image_path) if image_path else None, 
                              args.language)
    
    elif args.mode == "separate":
        # First transcribe, then generate query
        transcription = transcribe_audio(args.url, str(audio_path), args.language)
        if transcription:
            generate_query(args.url, transcription, 
                          str(image_path) if image_path else None)
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 