#!/usr/bin/env python3
"""
Launcher script for the VoiceQuery API.
"""
import argparse
import os
import sys
import uvicorn
from dotenv import load_dotenv

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="VoiceQuery API Server")
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the API server on"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to run the API server on"
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    parser.add_argument(
        "--workers", 
        type=int, 
        default=1, 
        help="Number of worker processes"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the API server."""
    # Load environment variables
    load_dotenv()
    
    # Override with environment variables if set
    args = parse_arguments()
    host = os.getenv("API_HOST", args.host)
    port = int(os.getenv("API_PORT", args.port))
    
    print(f"Starting VoiceQuery API server...")
    print(f"API will be available at http://{host}:{port}")
    
    if host == "0.0.0.0":
        print(f"Local access: http://localhost:{port}")
    
    # Start the uvicorn server
    try:
        uvicorn.run(
            "api:app",
            host=host,
            port=port,
            reload=args.reload,
            workers=args.workers
        )
    except KeyboardInterrupt:
        print("\nShutting down VoiceQuery API server...")
    except Exception as e:
        print(f"Error starting the API server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 