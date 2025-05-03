"""
whisper-query-parser API - REST API for the whisper-query-parser service.

This module provides REST API endpoints to transcribe audio,
process images, and generate structured queries for e-commerce applications.
"""
import os
import tempfile
import shutil
import time
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
import json

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Import core components from our application
from utils.audio_processing import load_audio
from utils.transcription import WhisperTranscriber
from utils.query_generation import QueryGenerator

# Load environment variables
load_dotenv()

# Initialize the transcriber with the model from .env or default to "base"
model_name = os.getenv("WHISPER_MODEL", "base")
transcriber = WhisperTranscriber(model_name=model_name)

# Initialize QueryGenerator (will use API key from .env)
try:
    query_generator = QueryGenerator()
except ValueError as e:
    print(f"Warning: {str(e)}")
    print("Query generation will be disabled.")
    query_generator = None

# Create FastAPI app
app = FastAPI(
    title="whisper-query-parser API",
    description="API for transcribing audio and generating structured queries for e-commerce",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Start time for uptime calculation
start_time = time.time()

# Define response models
class TranscriptionResponse(BaseModel):
    success: bool
    transcription: str
    error: Optional[str] = None

class QueryResponse(BaseModel):
    success: bool
    query: Optional[Dict[str, Any]] = None
    transcription: Optional[str] = None
    error: Optional[str] = None

class FullProcessResponse(BaseModel):
    success: bool
    transcription: Optional[str] = None
    query: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    uptime: float
    whisper_model: str
    query_generation_available: bool
    version: str

# Utility functions
def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    """
    Save an uploaded file to a temporary location.
    
    Args:
        upload_file: The uploaded file to save
        
    Returns:
        Path to the saved temporary file
    """
    try:
        suffix = Path(upload_file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
        return tmp_path
    finally:
        upload_file.file.close()

def cleanup_tmp_file(file_path: Path):
    """Remove a temporary file."""
    try:
        os.unlink(file_path)
    except Exception as e:
        print(f"Error cleaning up temp file {file_path}: {e}")

def check_query_generator_available():
    """Check if query generator is available and raise HTTP exception if not."""
    if query_generator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Query generation is not available. Please check API key configuration."
        )
    return query_generator

# Endpoints
@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": "whisper-query-parser API",
        "version": "1.0.0",
        "description": "API for transcribing audio and generating structured queries"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API status."""
    return {
        "status": "healthy",
        "uptime": time.time() - start_time,
        "whisper_model": model_name,
        "query_generation_available": query_generator is not None,
        "version": "1.0.0"
    }

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    Transcribe an audio file using Whisper.
    
    Args:
        audio_file: The audio file to transcribe
        language: Optional language code for transcription
        
    Returns:
        JSON response with transcription result
    """
    if not audio_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No audio file provided"
        )
    
    try:
        # Save uploaded file to temp location
        temp_file = save_upload_file_tmp(audio_file)
        background_tasks.add_task(cleanup_tmp_file, temp_file)
        
        # Transcribe the audio
        audio_data = load_audio(str(temp_file))
        result = transcriber.transcribe(audio_data, language=language)
        
        return {
            "success": True,
            "transcription": result.text
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during transcription: {str(e)}"
        )

@app.post("/generate-query", response_model=QueryResponse)
async def generate_query(
    background_tasks: BackgroundTasks,
    transcription: str = Form(...),
    image: Optional[UploadFile] = File(None),
    generator: QueryGenerator = Depends(check_query_generator_available)
):
    """
    Generate a structured query from transcribed text and an optional image.
    
    Args:
        transcription: The transcribed text to process
        image: Optional image file
        
    Returns:
        JSON response with generated query
    """    
    image_path = None
    try:
        # Save image to temp location if provided
        if image and image.filename:
            temp_image = save_upload_file_tmp(image)
            image_path = str(temp_image)
            background_tasks.add_task(cleanup_tmp_file, temp_image)
        
        # Generate query from transcription and image
        query_json = generator.generate_query(transcription, image_path)
        
        return {
            "success": True,
            "query": query_json,
            "transcription": transcription
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating query: {str(e)}"
        )

@app.post("/process", response_model=FullProcessResponse)
async def process_audio_to_query(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    image: Optional[UploadFile] = File(None),
    language: Optional[str] = Form(None),
    generator: QueryGenerator = Depends(check_query_generator_available)
):
    """
    Process audio file and optional image into a structured query.
    This is a convenience endpoint that combines transcription and query generation.
    
    Args:
        audio_file: The audio file to transcribe
        image: Optional image file
        language: Optional language code for transcription
        
    Returns:
        JSON response with transcription and query
    """
    if not audio_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No audio file provided"
        )
    
    audio_temp_file = None
    image_temp_file = None
    
    try:
        # Save uploaded files to temp location
        audio_temp_file = save_upload_file_tmp(audio_file)
        background_tasks.add_task(cleanup_tmp_file, audio_temp_file)
        
        image_path = None
        if image and image.filename:
            image_temp_file = save_upload_file_tmp(image)
            image_path = str(image_temp_file)
            background_tasks.add_task(cleanup_tmp_file, image_temp_file)
        
        # Step 1: Transcribe the audio
        audio_data = load_audio(str(audio_temp_file))
        result = transcriber.transcribe(audio_data, language=language)
        transcription = result.text
        
        # Step 2: Generate query from transcription and image
        query_json = generator.generate_query(transcription, image_path)
        
        return {
            "success": True,
            "transcription": transcription,
            "query": query_json
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "transcription": None,
            "query": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Generic exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": f"Unexpected error: {str(exc)}",
            "transcription": None,
            "query": None
        }
    )

if __name__ == "__main__":
    # Run the FastAPI app with uvicorn when script is executed directly
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port) 