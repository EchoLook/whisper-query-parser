"""
Query generation module for processing transcribed text with Gemini.

This module implements functionality to parse transcribed speech into structured
API queries using Google's Gemini model.
"""
import os
import json
from typing import Dict, Any, Optional, Union
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class QueryGenerator:
    """
    A class to generate structured queries from transcribed text using Gemini.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the QueryGenerator with Google API credentials.
        
        Args:
            api_key: Google AI API key (will use environment variable if not provided)
        """
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Either provide it as a parameter or "
                "set the GOOGLE_API_KEY environment variable in the .env file."
            )
            
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Get the multimodal model for text+image processing
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def generate_query(self, transcript: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a structured query from transcribed text and optional image.
        
        Args:
            transcript: The transcribed speech text
            image_path: Optional path to an image file to include in the context
        
        Returns:
            A dictionary containing the structured query
        """
        # Prepare the prompt with detailed instructions
        prompt = [
            "Transform the following transcribed speech into a structured query for a fashion e-commerce API.",
            "The result should be a simple JSON object that captures the key product requirements.",
            "Descriptions for the products should be concise and to the point, avoid adding properties like same as the image, just use the color of the product in the image, descriptions cant be FC Barcelona T-shirt, FC Barcelona Jersey, etc.",
            "For clothing items, extract: product type, color, price range if mentioned, and any other relevant attributes.",
            "If the user mentions modifications to items shown in the image, make those changes explicit in the query.",
            "If the user says something like I want this with the same color, make that change explicit in the query after watching the product color on the image.",
            "Focus only on actionable shopping criteria and ignore conversational elements.",
            f"\nTranscribed text: {transcript}\n",
            "Return ONLY a valid JSON object with no additional explanation, fields or text.",
            "The JSON should be formatted as follows:",
            "```json",
            "{"
            "  \"items\": ["
            "    {\"description\": \"string\", \"max_price\": number},"
            "    {\"description\": \"string\", \"max_price\": number}"
            "  ]"
            "}"
            "```"
        ]
        
        # Create content list for the model
        content = ["\n".join(prompt)]
        
        # Add image if provided
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                content.append(img)
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Generate a response from Gemini
        try:
            response = self.model.generate_content(content)
            
            # Extract JSON from the response text
            response_text = response.text
            
            # Clean up the response to extract only valid JSON
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse the JSON response
            try:
                query_data = json.loads(response_text)
                return query_data
            except json.JSONDecodeError:
                # If we can't parse the JSON, return a formatted error response
                return {
                    "error": "Could not parse response as JSON",
                    "transcript": transcript,
                    "raw_response": response_text[:200]  # Include part of the raw response for debugging
                }
            
        except Exception as e:
            return {
                "error": f"Failed to generate query: {str(e)}",
                "transcript": transcript
            }

    def generate_query_text(self, transcript: str, image_path: Optional[str] = None) -> str:
        """
        Generate a structured query as a formatted JSON string.
        
        Args:
            transcript: The transcribed speech text
            image_path: Optional path to an image file to include in the context
            
        Returns:
            Formatted JSON string containing the structured query
        """
        query_data = self.generate_query(transcript, image_path)
        
        # Always return a valid JSON string
        try:
            return json.dumps(query_data, indent=2, ensure_ascii=False)
        except Exception as e:
            # Provide a fallback in case of any serialization errors
            return json.dumps({
                "error": f"Error serializing response: {str(e)}",
                "transcript": transcript
            }, indent=2) 